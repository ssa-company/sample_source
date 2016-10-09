/* 
 * File:   antitheft_enc.h
 * Author: soldatov
 *
 * Created on 21 Июль 2014 г., 11:12
 */

#ifndef ANTITHEFT_PB_CRC_H
#define	ANTITHEFT_PB_CRC_H

int SearchCrcDataMarker     (char * buffer, 
                            int length);

int SearchCrcCodeMarker     (char * buffer, 
                            int length);

int CalcCRC32               (char * buffer, 
                            int length);

#endif	/* ANTITHEFT_PB_ENC_H */