# Content Generation

This directory contains scripts and resources used to generate the module content in this collection.

While the module_utils are manually written and maintained, the modules themselves are generated using these scripts and an API spec, and then the documentation is enriched using LLMs.

*Note*: The scripts in this directory are almost entirely generated using AI.

### General Workflow

The general workflow is:
1. Generate a module
2. Run/Generate tests
3. Ensure formatting/sanity
4. Validate other API version compatibility

## AI Quickstart

There are a few AI agent skills at /.agents/skills/ that can be used for this purpose.

The skills will generate the module, enrich the documentation using an LLM, perform formatting/sanity checks with black/ansible-test, and generate tests if needed.

## Manual Quickstart

To generate a module manually, run:

```bash
python content_generation/generate_module.py vcenter_datacenter --spec-version '9.1.0'
```

The API spec version must already exist in `content_generation/api_specs/`.

You should run `black .` after generating the module to format it correctly.

Review the module and fill in the required descriptions, EXAMPLES, and RETURNS. Or use the ansible-module-doc-review AI skill

Finally, validate the module against other API specs:

```bash
python content_generation/validate_api_compatibility.py --target '8.0.2'
```

## Generating Tests

If tests do not exist for the module, you can generate them using the /.agents/skills/generate-integration-tests and /.agents/skills/generate-unit-tests skills. These instruct the AI agent to generate passing tests based on the API spec.

While there are guidelines and scripts to help ensure a certain quality baseline, it is best to review them yourself to ensure all desired scenarios are tested and assertions make sense.

Once tests have been generated, I recommend you run them yourself, format them with black, and run sanity tests to make sure everything is green. The AI agent can help, but it tends to struggle if you ask it to do everything at once.

## Scripts

Each script has detailed documenatation and examples in the script itself.

### get_api_endpoints_for_module

This script parses a given API spec and outputs the relevant endpoints, arguments, and schemas for a specific module. It can output multiple formats for human or script consumption.

This script does not usually need to be run directly, and is run automatically as a first step by `generate_module.py`

### format_api_endpoints_for_module_generation

This script takes the output from get_api_endpoints_for_module.py and formats them into a YAML document that can be more easily used in module generation.

This script does not usually need to be run directly, and is run automatically as a second step by `generate_module.py`

### generate_module

This is the main script for generating modules. It takes the YAML document output by format_api_endpoints_for_module_generation.py and creates a basic, functioning module. It does its best to populate the module with documentation, but leaves some fields blank.

### fetch_vsphere_openapi_spec

This script can get an OpenAPI spec from Broadcom and place it in this repo. It is mainly called by AI agents using the fetch-vsphere-openapi-spec skill in /.agents/skills/

### generate_openapi_mocks

This script is used to generate OpenAPI spec files that are used in integration test mocks. The integration tests will setup a mock server that should respond as described by the specs, and make testing the modules possible without disrupting a live vCenter environment.

### validate_api_compatibility

This script is used to check if a module is compatible with other versions of the API besides the one that was used to generate the module. It will update the module notes if the module is compatible with the target API spec.

For example, if a module was generated from version 9, you may want to validate if it is compatible with version 7 and 8. The version of the API you are trying to validate must be present in the api_specs/ directory.
