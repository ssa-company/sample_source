// Автор кода под Windows Сергей Усков (Sergey.Uskov@safenet-inc.com, uskov@smtp.ru)
//*****************************************************************************
// Модификация под Linux - Сергей Солдатов (soldatov@l-on.ru)

#include "antitheft-pb.h"

char * LastDsc = NULL;

//////////////////////////////////////////////////////////////////////////////////////////////
//  Процедура ищет в целевом файле структуры, описывающие данные, которые необходимо зашифровать.

int SearchCrcDataMarker(char * buffer, int length) {
    int i, descriptor_raw, data_raw, done = 0;
    char * startPtr;
    PCrcDataMrk marker;
    PCrcDsc descriptor;

    for (i = 0; i < length; i++) {
        startPtr = (char *) memchr(buffer + i, FirstChar, length - i);
        if (startPtr == NULL) continue;
        i = startPtr - buffer;
        if (!memcmp(startPtr, CrcDataSig, SignatureLength)) {

            // Найден маркер, описывающий данные, выводим дампы маркера и данных.
            done++;
            marker = (PCrcDataMrk) startPtr;
            descriptor_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->CrcDscAddr);
            descriptor = (PCrcDsc) (buffer + descriptor_raw);
            data_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->Addr);
            printf("Marker found --> Region ID = %04d, Region length = %d(%Xh) byte(s)\n", marker->Id, marker->Length, marker->Length);
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("Descriptor_RAW . ");
            PrintDump(buffer, descriptor_raw); // Дескриптор
            printf("DATA_RAW ....... ");
            PrintDump(buffer, data_raw); // Данные

            // Заполняем данными структуру-описатель, выводим расчитанное значение контрольной суммы.
            printf("> Calculation CRC ................................ ");
            descriptor->NextDsc = LastDsc; // Адрес последнего найденного дескриптора
            LastDsc = (char *) marker->CrcDscAddr; // Теперь последний - текущий дескриптор
            descriptor->Addr = (char *) marker->Addr;
            descriptor->Length = marker->Length;
            descriptor->OrgCrc = CalcCRC32(buffer + data_raw, descriptor->Length);
            descriptor->CurrCrc = 0;
            descriptor->Id = marker->Id;
            descriptor->ValidateFlag = FALSE;
            printf("%08Xh\n", descriptor->OrgCrc);

            // Заполняем мусором маркер.
            printf("> Marker's content replacement ................... ");
            ReplaceData(startPtr, sizeof (CrcDataMrk));
            printf("Ok\n");

            // Выводим дампы маркера и описателя.
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("Descriptor_RAW . ");
            PrintDump(buffer, descriptor_raw); // Дескриптор
            printf("\n \n");
        }
    }
    return done;
}


//////////////////////////////////////////////////////////////////////////////////////////////
//  Процедура ищет в целевом файле структуры, описывающие данные, которые необходимо зашифровать.

int SearchCrcCodeMarker(char * buffer, int length) {
    int i, descriptor_raw, code_raw, code_len, done = 0;
    char * startPtr;
    PCrcCodeMrk marker;
    PCrcDsc descriptor;

    for (i = 0; i < length; i++) {
        startPtr = (char *) memchr(buffer + i, FirstChar, length - i);
        if (startPtr == NULL) continue;
        i = startPtr - buffer;
        if (!memcmp(startPtr, CrcCodeSig, SignatureLength)) {

            // Найден маркер, описывающий код, выводим дампы маркера и кода.
            done++;
            marker = (PCrcCodeMrk) startPtr;
            descriptor_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->DescriptorAddr);
            descriptor = (PCrcDsc) (buffer + descriptor_raw);
            code_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->StartAddr);
            code_len = marker->EndAddr - marker->StartAddr;
            printf("Marker found --> Region ID = %04d, Region length = %d(%Xh) byte(s)\n", marker->Id, code_len, code_len);
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("Descriptor_RAW . ");
            PrintDump(buffer, descriptor_raw); // Дескриптор
            printf("CODE_RAW ....... ");
            PrintDump(buffer, code_raw); // Код

            // Заполняем данными структуру-описатель, выводим расчитанное значение контрольной суммы.
            printf("> Calculation CRC ................................ ");
            descriptor->NextDsc = LastDsc; // Адрес последнего найденного дескриптора
            LastDsc = (char *) marker->DescriptorAddr; // Теперь последний - текущий дескриптор
            descriptor->Addr = (char *) marker->StartAddr;
            descriptor->Length = code_len;
            descriptor->OrgCrc = CalcCRC32(buffer + code_raw, descriptor->Length);
            descriptor->CurrCrc = 0;
            descriptor->Id = marker->Id;
            descriptor->ValidateFlag = FALSE;
            printf("%08Xh\n", descriptor->OrgCrc);

            // Заполняем мусором маркер.
            printf("> Marker's content replacement ................... ");
            ReplaceCode(startPtr, sizeof (CrcCodeMrk));
            printf("Ok\n");

            // Выводим дампы маркера и описателя.
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("Descriptor_RAW . ");
            PrintDump(buffer, descriptor_raw); // Дескриптор
            printf("\n \n");
        }
    }
    return done;
}
