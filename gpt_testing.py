from openai import OpenAI

client = OpenAI(api_key = r"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")

# response = client.responses.create(
#     model="gpt-4o-mini-2024-07-18",
#     tools=[{ "type": "web_search_preview" }],
#     input="Search www.rightmove.co.uk for house share, to rent properties listed today in W2.",
# )

# print(response.output_text)

response = client.responses.create(
model="gpt-4o-mini-2024-07-18",
input=[
    {
        "role" : "developer",
        "content" : "Guess the location based on the data, and return a full approximate postcode only, with nothing else within the response."
    }, 
    {
        "role" : "user",
        "content" : "['Delorme Street, Hammersmith, London, W6', 'Apartment', '2 bathrooms', 'PLEASE NOTE THAT THIS PROPERTY IS ONLY SUITABLE FOR A FAMILY. A beautifully presented three bedroom, two bathroom split level period conversion flat with a private south facing roof terrace in this highly sought after residential road. The property which is stylish and well maintained throughout ...', '£2,900 pcm', 'Lawson Rutter']"
    }
    ]
)

postcode = response.output_text
print(postcode)