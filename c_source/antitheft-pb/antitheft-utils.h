/* 
 * File:   antitheft_utils.h
 * Author: soldatov
 *
 * Created on 21 Июль 2014 г., 10:50
 */

#ifndef ANTITHEFT_UTILS_H
#define	ANTITHEFT_UTILS_H

#define SignatureLength             7
#define FirstChar                   '-'

gboolean SavingImageBaseValue       (char * buffer, 
                                    int length);

uint32_t vaddr32_to_file_offset     (char * buffer, 
                                    int length, 
                                    uint32_t vaddr);

void ConsolErrMsg                   (char * format, ...);

void PrintDump                      (char * buffer, 
                                    const uint32_t offset);

void ReplaceData                    (char * buffer, 
                                    uint32_t length);

void ReplaceCode                    (char * buffer, 
                                    uint32_t length);

#endif	/* ANTITHEFT_UTILS_H */

