/* 
 * File:   antitheft.c
 * Author: soldatov
 *
 * Created on 25 Июнь 2014 г., 14:56
 */

#include <glib/gstdio.h>
#include <fcntl.h>
#include <pwd.h>
#include <sys/mman.h>

#include "antitheft-pb.h"

gboolean verbose_flag;
gint verbose_level = 0;
gboolean key_check;
gchar * target_file;
gboolean ImageBaseSig_flag;
gboolean CstEncDataSig_flag;
gboolean KeyEncDataSig_flag;
gboolean CrcDataSig_flag;
gboolean CrcCodeSig_flag;

static GOptionEntry entries[] =
{
  { "verbose",  'v', 0, G_OPTION_ARG_NONE,      &verbose_flag,          "Be verbose", NULL },
  { "verbose-level", 0, 0, G_OPTION_ARG_INT,    &verbose_level,         "Verbose level 0..1",    "0" },
  { "target",   't', 0, G_OPTION_ARG_FILENAME,  &target_file,           "Target file", NULL },
  { "checkkey", 'k', 0, G_OPTION_ARG_NONE,      &key_check,             "Check that Hasp key present in system", NULL },
  { "img",        0, 0, G_OPTION_ARG_NONE,      &ImageBaseSig_flag,     "Search ImageBaseSign", FALSE },
  { "ceds",       0, 0, G_OPTION_ARG_NONE,      &CstEncDataSig_flag,    "Search CstEncDataSig", FALSE },
  { "keds",       0, 0, G_OPTION_ARG_NONE,      &KeyEncDataSig_flag,    "Search KeyEncDataSig", FALSE },
  { "cds",        0, 0, G_OPTION_ARG_NONE,      &CrcDataSig_flag,       "Search CrcDataSig", FALSE },
  { "ccs",        0, 0, G_OPTION_ARG_NONE,      &CrcCodeSig_flag,       "Search CrcCodeSig", FALSE },
  { NULL }
};

// Application log handler
// meaning of user_date current is antitheft
// propably antitheft for deliver facility and other parm.
static void _app_log_handler(const gchar *log_domain,
                     GLogLevelFlags log_level,
                     const gchar *message,
                     gpointer user_data )
{
    FILE * log;
    GDateTime * now;
    gchar * now_str;
    g_print("%s\n",message);

    log = fopen(ANTITHEFT_DEFLOGFILE, "a");
    now = g_date_time_new_now_local();
    now_str = g_date_time_format(now, "%b %d %T");
    g_fprintf(log, "%s %s: %s\n", now_str, (getpwuid(getuid())) -> pw_name, (message));
    g_free(now_str);
    g_date_time_unref(now);
    fclose(log);
    
    return;
}

int main(int argc, char** argv) {
    
    GError *error = NULL;
    GOptionContext *context;
    void    * lpFileMap;
    int fd, Done, MarkersDone = 0;
    struct stat s;

    // Setup firstime handler, while antitheft undefined G_LOG_DOMAIN
    GHashTable * log_hndl_table = NULL;
    set_verbose_many(verbose_flag, verbose_level, _app_log_handler, &log_hndl_table, NULL, "NULL", "TvssLib", "AntitheftLib", NULL);

    // Parse options from command line
    gchar * info = g_strdup_printf("- postbuild utility %s", VERSION);
    context = g_option_context_new (info);
    g_option_context_set_summary(context,ANTITHEFT_OPTION_SUMMARY);
    g_option_context_set_description(context, ANTITHEFT_OPTION_DESCRIPTION);
    g_option_context_add_main_entries (context, entries, NULL);
    g_option_context_set_help_enabled (context, TRUE);

    if (!g_option_context_parse (context, &argc, &argv, &error))
    {
        g_critical("Option parsing failed: %s\n", error->message);
        g_option_context_free(context);
        g_error_free(error);
        exit (EXIT_FAILURE);
    }

    g_option_context_free(context);
    g_free(info);
    
    if (key_check) {
        if (!CheckFeatureExt(DEFAULT_NULL_FEAUTURE, FALSE))
        {
            g_debug("HASP key not found. Application close.\n");
            exit(EXIT_HASP);
        }
        exit(EXIT_SUCCESS);
    }
    
    if (target_file) {
        // Открываем целевой файл
        printf("Open the target file ........................... %s -> ", target_file);
        fd = open(target_file, O_RDWR);
        if (fd == -1) {
            printf("Error\n");
            g_critical("Can not open file %s", target_file);
            exit (EXIT_FAILURE);
        }
        printf("Ok\n");
    }
    else {
        g_critical("No target file. Usage: antitheft <target file>.");
        exit (EXIT_FAILURE);
    }
    
    // Определяем размер файла
    fstat(fd, &s);
    printf("File size ...................................... %d bytes\n", (int)s.st_size);

    // Выполняем отображение файла на память. В переменную lpFileMap будет записан указатель на отображаемую область памяти
    printf("Maps a view of a file into the address space ... ");
    lpFileMap = mmap(NULL, s.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, (off_t)0);
    if(lpFileMap == MAP_FAILED) {
        printf("Error\n");
        g_critical("Can not maps file %s into memory", target_file);
        exit (EXIT_FAILURE);
    }	
    printf("Ok\n");

    if (ImageBaseSig_flag){
        printf("\n\n---------------------------- ImageBase Markers processing ---------------------------------\n\n");
        if (!SavingImageBaseValue((char *)lpFileMap, s.st_size))
            printf("Markers not found.\n \n");
    }
    if (CstEncDataSig_flag) {
        printf("\n\n------------------------ Custom Encrypt Data Markers processing ----------------------------\n\n");
        Done = SearchCustomEncDataMarker((char *)lpFileMap, s.st_size);
        if(!Done) printf("Markers not found.\n \n");
        MarkersDone += Done;

        printf("\n------------------ Processing is completed. Total %.2d marker(s) are found --------------------\n\n", MarkersDone);
    }

    if (KeyEncDataSig_flag) {
        printf("\n\n------------------------ Key Encrypt Data Markers processing ----------------------------\n\n");
        Done = SearchKeyEncDataMarker((char *)lpFileMap, s.st_size);
        if(!Done) printf("Markers not found.\n \n");
        MarkersDone += Done;

        printf("\n------------------ Processing is completed. Total %.2d marker(s) are found --------------------\n\n", MarkersDone);
    }
    
    if (CrcDataSig_flag) {
        printf("\n\n------------------------ CRC32 Data Markers processing ----------------------------\n\n");
        Done = SearchCrcDataMarker((char *)lpFileMap, s.st_size);
        if(!Done) printf("Markers not found.\n \n");
        MarkersDone += Done;

        printf("\n------------------ Processing is completed. Total %.2d marker(s) are found --------------------\n\n", MarkersDone);
    }

    if (CrcCodeSig_flag) {
        printf("\n\n------------------------ CRC32 Code Markers processing ----------------------------\n\n");
        Done = SearchCrcCodeMarker((char *)lpFileMap, s.st_size);
        if(!Done) printf("Markers not found.\n \n");
        MarkersDone += Done;

        printf("\n------------------ Processing is completed. Total %.2d marker(s) are found --------------------\n\n", MarkersDone);
    }   
    
    // Отменяем отображение файла и освобождаем идентификатор созданного объекта-отображения
    printf("\nClose the target file .......................... ");
    munmap(lpFileMap, s.st_size);
    close(fd);
    printf("Ok\n \n");
    
    return (EXIT_SUCCESS);
}
