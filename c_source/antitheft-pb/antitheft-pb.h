/* 
 * File:   antitheft_pb.h
 * Author: soldatov
 *
 * Created on 18 Июль 2014 г., 16:55
 */

#ifndef ANTITHEFT_PB_H
#define	ANTITHEFT_PB_H

#include "antitheft.h"
#include "tvrs.h"

#include "antitheft-pb-enc.h"
#include "antitheft-pb-crc.h"
#include "antitheft-utils.h"
#include "antitheft-pb_version.h"

#define ANTITHEFT_OPTION_SUMMARY      "Post-Build Data Encryption Tools"
#define ANTITHEFT_OPTION_DESCRIPTION  "This program is property of LightON\n"\
                                      "Report bugs to <bug-make@l-on.ru>"
#define ANTITHEFT_DEFLOGFILE          "antitheft.log"

// Application logging definition
#define ANTITHEFT_LOG_LEVEL_QUIETLY   G_LOG_LEVEL_CRITICAL|G_LOG_LEVEL_WARNING|G_LOG_FLAG_FATAL|G_LOG_FLAG_RECURSION
#define ANTITHEFT_LOG_LEVEL_MAIN      G_LOG_LEVEL_CRITICAL|G_LOG_LEVEL_WARNING|G_LOG_FLAG_FATAL|G_LOG_FLAG_RECURSION|G_LOG_LEVEL_MESSAGE
#define ANTITHEFT_LOG_LEVEL_DEBUG     G_LOG_LEVEL_MASK

#endif	/* ANTITHEFT_H */

