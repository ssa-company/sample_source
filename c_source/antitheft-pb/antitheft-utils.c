// Автор кода под Windows Сергей Усков (Sergey.Uskov@safenet-inc.com, uskov@smtp.ru)
//*****************************************************************************
// Модификация под Linux - Сергей Солдатов (soldatov@l-on.ru)
#include <libelf.h>

#include "antitheft-pb.h"

//////////////////////////////////////////////////////////////////////////////////////////////
//  Процедура замещает содержимое указанного буфера с кодом на "мусор". 

void ReplaceCode(char * buffer, uint32_t length) {
    int i;

    if (length > 2 && length < 128) {
        // Если длина маркера допускает использование инструкции короткого перехода, то формируем 
        // jmp short вокруг всего маркера, а внутренности маркера забиваем мусором.
        buffer[0] = 0xEB; // Опкод jmp short ххх
        buffer[1] = (char) (length - 2); // Вычисляем операнд инструкции
        for (i = 2; i < length; i++) buffer[i] = rand() % 0xFF; // Генерируем мусор
    } else {
        // Если маркер очень короткий или слишком длинный для использования короткого перехода, забиваем его NOP'ами, 
        for (i = 0; i < length; i++) buffer[i] = 0x90;
    }
}

//  Процедура замещает содержимое указанного буфера с данными на "мусор". 

void ReplaceData(char * buffer, uint32_t length) {
    uint32_t i;
    for (i = 0; i < length; i++) {
        buffer[i] = rand() % 0xFF; // Генерируем мусор
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////
// Процедура переводит VA-адрес объекта в целевом файле в смещение относительно начала этого 
// файла, загруженного в буфер по адресу Base. Функция для 32 битной системы

uint32_t vaddr32_to_file_offset(char * buffer, int length, uint32_t vaddr) {
    int err;
    const char *errmsg;
    Elf * e;
            
    if (elf_version(EV_CURRENT) == EV_NONE)
    {
        err = elf_errno();
	if (err != 0) errmsg = elf_errmsg(err);
        
        g_warning("ELF library too old: %s", errmsg);
    }
    e = elf_memory(buffer, length);
    
    if (!e) 
    {
        err = elf_errno();
	if (err != 0) errmsg = elf_errmsg(err);
        
        g_warning("Cant mapped memory: %s", errmsg);
    }
    uint32_t offset = 0;

    Elf_Scn * scn = NULL;
    while ((scn = elf_nextscn(e, scn)) != NULL) {
        Elf32_Shdr * shdr = elf32_getshdr(scn);
        if (vaddr >= shdr->sh_addr && (vaddr <= (shdr->sh_addr + shdr->sh_size))) {
            offset = shdr->sh_offset + (vaddr - shdr->sh_addr);
            break;
        }
    }

    elf_end(e);
    return offset;
}

//////////////////////////////////////////////////////////////////////////////////////////////
//  Вывод сообщения в черной рамке (для заметности) в окно вывода.

void ConsolErrMsg(char * format, ...) {
    char buffer[128];
    va_list arg_ptr;
    uint32_t i, gap, len = 92;

    va_start(arg_ptr, format);
    vsprintf(buffer, format, arg_ptr);
    va_end(arg_ptr);

    gap = (len - 2 - strlen(buffer)) / 2;

    printf("\n \n");
    for (i = 0; i < len; i++) printf("\xdb");
    printf("\n");
    for (i = 0; i < gap; i++) printf("\xdb");
    printf(" %s ", buffer);
    if ((len - strlen(buffer)) % 2) printf(" ");
    for (i = 0; i < gap; i++) printf("\xdb");
    printf("\n");
    for (i = 0; i < len; i++) printf("\xdb");
    printf("\n \n");
}

//////////////////////////////////////////////////////////////////////////////////////////////
//  Процедура печатает HEX/ASCII-дамп параграфа памяти (16 байт) с указанного смещения.

void PrintDump(char * buffer, const uint32_t offset) {
    uint32_t i;

    printf("%08X ", offset);
    for (i = 0; i < 16; i++) printf(" %02X", (char unsigned) buffer[offset + i]);
    printf("  ");
    for (i = 0; i < 16; i++) printf("%c", buffer[offset + i] > 0x1F && buffer[offset + i] < 0xFF ? buffer[offset + i] : '.');
    printf("\n");
}

//////////////////////////////////////////////////////////////////////////////////////////////
// Процедура ищет в целевом файле дескриптор-контейнер для сохранения оригинального значения
// ImageBase, т.к. в случае использования технологии ASLR, оригинальное значение ImageBase
// произвольно перезаписывается системным загрузчиком. 

gboolean SavingImageBaseValue(char * buffer, int length) {
    int i;
    char * startPtr;
    POrgPE descriptor;

    Elf32_Ehdr * ehdr = (Elf32_Ehdr *) buffer;
    g_debug("Entry point virtual address %p\n", (void *) ehdr ->e_entry);

    for (i = 0; i < length; i++) {
        startPtr = (char *) memchr(buffer + i, FirstChar, length - i);
        if (startPtr == NULL) continue;
        i = startPtr - buffer;
        if (!memcmp(startPtr, OrgPESig, SignatureLength)) {

            // Найден дескриптор-контейнер для хранения ImageBase.
            printf("\n-------------------------- Saving the ImageBase original value -----------------------------\n \n");

            descriptor = (POrgPE) (buffer + i);
            printf("Descriptor_RAW . ");
            PrintDump(buffer, i); // Маркер

            // Сохраняем оригинальное значение ImageBase.
            printf("> Saving ImageBase original value ................ ");
            descriptor->ImageBase = (int) ehdr ->e_entry;
            printf("Ok\n");

            // Заполняем мусором сигнатуру дескриптора.
            printf("> Descriptor's signature replacement ............. ");
            ReplaceData(startPtr, SignatureLength);
            printf("Ok\n");

            // Выводим дамп дескриптора после обработки.
            printf("Descriptor_RAW . ");
            PrintDump(buffer, i); // Маркер
            printf("\n \n");
            return TRUE;
        }
    }
    return FALSE;
}