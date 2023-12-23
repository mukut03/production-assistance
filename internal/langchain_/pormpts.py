from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

summary_schema = ResponseSchema(name="summary",
                                     description="A short summary of the script")
characters_schema = ResponseSchema(name="characters",
                                     description="A summary of all the characters in the script")
props_schema = ResponseSchema(name="props",
                               description="A summary of all the props in the script")


response_schemas = [summary_schema,
                    characters_schema,
                    props_schema]

req_parser = StructuredOutputParser.from_response_schemas(response_schemas)

req_template = """\
From the following pieces of context, extract the following information and format the response as a JSON object with the following keys:
{context}


summary: Create a summary of the entire script \
Include specific information from the script to support your summary \
This should be extracted as a python string \


characters: How many characters are in this script?\
Create a summary including all characters \
Include any/all characteristics for all the characters \
This should be extracted as a python string \


props: What props are used in this script? \
Create a summary of all the props that are used in this script by any/all characters \
Include information about repeated props if possible \
This should be extracted as a python string \

Format the output as JSON with the following keys:
summary
characters
props

"""
