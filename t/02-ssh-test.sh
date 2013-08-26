#!/bin/bash

# Load testing framework
. ./testlib.sh

# Test setup
. ./test_setup.sh

TEST_SUITE_NAME="Test sshd_config template creation"

# Number of tests
TOTAL_TESTS=6

$TEMPLATE_MAKER -p $OF_PREFIX-kv-1.txt -f $OF_PREFIX-1.in \
    -o $OF_PREFIX-1.out -a $OF_PREFIX-2.out
assert_ran_ok "Basic template creation (chef) ran ok"
assert "Template file output" "diff -u $OF_PREFIX-1.cmp $OF_PREFIX-1.out"
assert "Attributes file output" "diff -u $OF_PREFIX-2.cmp $OF_PREFIX-2.out"

$TEMPLATE_MAKER -t ansible -p $OF_PREFIX-kv-1.txt -f $OF_PREFIX-1.in \
    -o $OF_PREFIX-3.out -a $OF_PREFIX-4.out
assert_ran_ok "Basic template creation (ansible) ran ok"
assert "Template file output" "diff -u $OF_PREFIX-3.cmp $OF_PREFIX-3.out"
assert "Attributes file output" "diff -u $OF_PREFIX-4.cmp $OF_PREFIX-4.out"

# Print results
report
