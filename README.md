## Idea behind the project: 
Take in an image, use an LLM to classify it according to some predefined features, then match the response to the closest song vector in our song database, which theoretically maps out a song for a given image.



Used the Cyanite API to tag music and store it in a vector database according to the queried Features. 

Leveraged Pinecone as our Vector DB. 

Utilized LLAVA (capable of chatting with images) as the LLM.

Flask was used for the APIs and React as the web App. 


<img width="1728" alt="Screenshot 2024-10-12 at 12 50 20 AM" src="https://github.com/user-attachments/assets/a32b5e35-65e5-4b85-9cf3-9202456aa50e">
