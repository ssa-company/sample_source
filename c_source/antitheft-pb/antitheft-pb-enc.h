/* 
 * File:   antitheft_pb_enc.h
 * Author: soldatov
 *
 * Created on 21 Июль 2014 г., 11:12
 */

#ifndef ANTITHEFT_PB_ENC_H
#define	ANTITHEFT_PB_ENC_H
    
int SearchKeyEncDataMarker      (char * buffer, 
                                int length);

int SearchCustomEncDataMarker   (char * buffer, 
                                int length);

#endif	/* ANTITHEFT_PB_ENC_H */

