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
    FILES=$DIR/*.py
    for f in $FILES; do
        python -m doctest $f
        assert_ran_ok "Python doctests - $f"
    done
}

cd ..
run_doctests .
run_doctests filters
run_doctests templatetype

# Print results
report
