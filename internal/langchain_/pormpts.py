from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate

number_of_chars_schema = ResponseSchema(name="number_of_chars",
                                        description="Number of unique characters")
number_of_props_schema = ResponseSchema(name="number_of_props",
                                        description="Number of unique props")
number_of_locations_schema = ResponseSchema(name="number_of_locations",
                                            description="Number of unique locations")
list_of_chars_schema = ResponseSchema(name="list_of_chars",
                                      description="List of unique characters")
list_of_props_schema = ResponseSchema(name="list_of_props",
                                      description="List of unique props")
list_of_locations_schema = ResponseSchema(name="list_of_locations",
                                          description="List of unique locations")
type_of_chars_schema = ResponseSchema(name="type_of_chars",
                                      description="Category of chars")
type_of_locations_schema = ResponseSchema(name="type_of_locations",
                                          description="Category of chars")
summary_schema = ResponseSchema(name="summary",
                                description="A short summary of the script")
characters_schema = ResponseSchema(name="characters",
                                   description="A summary of all the characters in the script")
props_schema = ResponseSchema(name="props",
                              description="A summary of all the props in the script")

sceneDesc_schema = ResponseSchema(name="sceneDesc",
                                  description="Descriptions for scenes in the script")

response_schemas = [number_of_chars_schema,
                    number_of_props_schema,
                    number_of_locations_schema,
                    list_of_chars_schema,
                    list_of_props_schema,
                    list_of_locations_schema,
                    type_of_chars_schema,
                    type_of_locations_schema,
                    summary_schema,
                    characters_schema,
                    props_schema,
                    sceneDesc_schema]

req_parser = StructuredOutputParser.from_response_schemas(response_schemas)

req_template = """\
From the following pieces of context, extract the following information and format the response as a JSON object with the following keys:
{context}

number_of_chars: Number of unique characters \
consider all characters mentioned in the script \
list_of_chars: Show a comma separated list of all characters \
type_of_chars: Classify the characters between Human being vs Animal, Man vs Woman, Aged vs Young \

number_of_props: Number of unique props \
list_of_props: Show a comma separated list of all props used \

number_of_locations: Number of unique locations \
list_of_locations: Show a comma separated list of all locations \
type_of_locations: for each location suggest a nearby site \

summary: Create a summary of the entire script as a story that adds context\
Include specific information from the script to support your summary \
If available, this should include the location(s) mentioned in the script
If available, this should include the time period(s) mentioned in th script
This should be extracted as a python string \

characters: How many characters are in this script?\
Create a summary including all characters \
Include any/all characteristics for all the characters \
This should be extracted as a python string \


props: What props are used in this script? \
Create a summary of all the props that are used in this script by any/all characters \
Include information about repeated props if possible \
This should be extracted as a python string \

sceneDesc: Come up with simple visual descriptions for some scenes in the script\
This could include information such as scene setting, time of day, location, etc \
Description should include which character is doing what \
Each description should be a string \
This should be organized in a dictionary \
The key should be the name of the scene \
The value should be a string containing a description for a scene \

Format the output as JSON with the following keys:
number_of_chars
number_of_props
number_of_locations
summary
characters
props
sceneDesc

"""

image_prompt = PromptTemplate(
    input_variables=["scene_desc", "summary", "characters", "props"],
    template="Create a prompt for DALL-E image generation that creates a depiction of a movie scene using all the information passed in, scene description: {scene_desc}, overall story summary: {summary}, characters: {characters}, and props:{props} In the final prompt, keep the scene description and the context separate. Put the scene description first, then include all the other information as context.  Explicitly state that there should not be any text in the images generated. Remeber, the maximum length for your response is 4000 characters",
)
