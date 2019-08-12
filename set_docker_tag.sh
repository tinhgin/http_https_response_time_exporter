#!/usr/bin/env bash
if [ -z "$CI_COMMIT_TAG" ]; then
    if [ "$CI_COMMIT_REF_NAME" == "master" ]; then
        export DOCKER_TAG=latest;
    else
        export DOCKER_TAG="$CI_COMMIT_REF_NAME"
    fi
else
    export DOCKER_TAG="${CI_COMMIT_TAG}";
fi