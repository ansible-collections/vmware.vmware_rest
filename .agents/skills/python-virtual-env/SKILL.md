---
name: python-virtual-env
description: Sets up a virtual environment that can be used for all python related tasks in this project.
---

# Skill: python-virtual-env

## Purpose

Create and activate a virtual environment that can be used when installing python packages and running commands.

## When to Invoke

TRIGGER when:
- Using a skill that requires python commands or has python dependencies
- A user asks to setup a virtual environment
- A user asks how to setup the local development environment

---

## Inputs

The user may specify the version of python they want to use. If it is not found on their local system, ask how they want to proceed.
The user may specify the virtual environment tool, or command, to use when creating a new virtual environment. If they do not specify, use `python -m venv ....`

## Workflow

Stop this skill immediately on failure, and report back to the user. Do not try to solve any errors during this stage.

1. Check if there is currently a virtual environment active.
2. If there is no active virtual environment, check if the directory '.venv' exists in the root of the repository. If it does not exist, create a new virtual environment named '.venv'
3. Activate the virtual environment in '.venv'. Try to activate the environment before any future python related commands.
