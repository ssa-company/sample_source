// Автор кода под Windows Сергей Усков (Sergey.Uskov@safenet-inc.com, uskov@smtp.ru)
//*****************************************************************************
// Модификация под Linux - Сергей Солдатов (soldatov@l-on.ru)
#include "antitheft-pb.h"

//////////////////////////////////////////////////////////////////////////////////////////////
// Процедура ищет в целевом файле маркеры, описывающие данные, которые необходимо зашифровать
// через ключ.

int SearchKeyEncDataMarker(char * buffer, int length) {
    uint32_t i, data_raw, done = 0;
    PKeyEncDataMrk marker;
    hasp_status_t status;
    char * startPtr;

    for (i = 0; i < length; i++) {
        startPtr = (char *) memchr(buffer + i, FirstChar, length - i);
        if (startPtr == NULL) continue;
        i = startPtr - buffer;
        if (!memcmp(startPtr, KeyEncDataSig, SignatureLength)) {

            // Найден маркер, описывающий данные, выводим дампы маркера и данных.
            done++;
            marker = (PKeyEncDataMrk) startPtr;
            data_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->Addr);
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("DATA_RAW ....... ");
            PrintDump(buffer, data_raw); // Данные

            // Зашифровываем данные. 
            printf("> Encrypt the target DATA ........................ ");
            status = KeyEncryptData(buffer + data_raw, marker->Length, marker->Feature, FALSE);
            if (status == HASP_STATUS_OK) {
                printf("Ok, DATA length %d(%Xh) byte(s)\n", marker->Length, marker->Length);

                // Заполняем мусором маркер.
                printf("> Marker's content replacement ................... ");
                ReplaceData(startPtr, sizeof (KeyEncDataMrk));
                printf("Ok\n");

                // Выводим дампы маркера и данных.
                printf("Marker_RAW ..... ");
                PrintDump(buffer, i);           // Маркер
                printf("DATA_RAW ....... ");
                PrintDump(buffer, data_raw);    // Данные
                printf("\n \n");

            } else {

                printf("LDK API Error #%d\n", status);
                ConsolErrMsg("Data key-encryption error #%d", status);
            }
        }
    }
    return done;
}

//////////////////////////////////////////////////////////////////////////////////////////////
// Процедура ищет в целевом файле маркеры, описывающие данные, которые необходимо зашифровать
// custom-алгоритмом.

int SearchCustomEncDataMarker(char * buffer, int length) {
    int i, data_raw, done = 0;
    PCstEncDataMrk marker;
    char * startPtr;
    for (i = 0; i < length; i++) {
        startPtr = memchr(buffer + i, FirstChar, length - i);
        if (startPtr == NULL) continue;
        i = startPtr - buffer;
        if (!memcmp(startPtr, CstEncDataSig, SignatureLength)) {

            // Найден маркер, описывающий данные, выводим дампы маркера и данных.
            done++;
            marker = (PCstEncDataMrk) startPtr;
            data_raw = vaddr32_to_file_offset(buffer, length, (uint32_t) marker->Addr);
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("DATA_RAW ....... ");
            PrintDump(buffer, data_raw); // Данные
            printf("DATA_LENGTH .... %d\n", marker->Length);

            // Зашифровываем данные. 
            printf("> Encrypt the target DATA ........................ ");
            CustomEncryptData(buffer + data_raw, marker->Length);
            printf("Ok, DATA length %d(%Xh) byte(s)\n", marker->Length, marker->Length);

            // Заполняем мусором маркер.
            printf("> Marker's content replacement ................... ");
            ReplaceData(startPtr, sizeof (CstEncDataMrk));
            printf("Ok\n");

            // Выводим дампы маркера и данных.
            printf("Marker_RAW ..... ");
            PrintDump(buffer, i); // Маркер
            printf("DATA_RAW ....... ");
            PrintDump(buffer, data_raw); // Данные
            printf("\n \n");
        }
    }
    return done;
}
