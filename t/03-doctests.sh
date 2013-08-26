#!/bin/bash

# Load testing framework
. ./testlib.sh

# Test setup
. ./test_setup.sh

TEST_SUITE_NAME="Run python doctests"

# Don't count the total number of tests
TOTAL_TESTS=

run_doctests() {
    DIR=$1
    cd $DIR
    FILES=*.py
    for f in $FILES; do
        python -m doctest $f
        assert_ran_ok "Python doctests - $DIR/$f"
    done
    cd - > /dev/null
}

cd ..
run_doctests .
run_doctests filter
run_doctests action
run_doctests templatetype

# Print results
report
