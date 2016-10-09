/*
 * File:   
 * Author: soldatov
 *
 * Created on 18.11.2014, 12:11:19
 */

#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>

#include "tests_utils.h"
 
/*
 * CUnit Test Suite
 */


int init_suite(void) {
    return 0;
}

int clean_suite(void) {
    return 0;
}

TEST_FUNCT(test1) {
    CU_ASSERT(2 * 2 == 4);
}

TEST_FUNCT(test2) {
    CU_ASSERT(2 * 3 == 5);
}

TEST_FUNCT(test3) {
    CU_ASSERT(2 * 9 == 18);
}

TEST_FUNCT(test4) {
    CU_ASSERT(2 * 7 == 14);
}

TEST_FUNCT (test5) {
    CU_ASSERT(2 * 7 == 19);
}

void runSuite(void) {
    CU_pSuite suite = CUnitCreateSuite("test1_timer");
    if (suite) {
        ADD_SUITE_TEST(suite, test1)
        ADD_SUITE_TEST(suite, test2)
        ADD_SUITE_TEST(suite, test3)
        ADD_SUITE_TEST(suite, test4)
        ADD_SUITE_TEST(suite, test5)
    }
}