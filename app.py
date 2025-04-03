from flask import Flask, request, jsonify, render_template
import groq

app = Flask(__name__)

# Set up Groq API key
groq_api_key = '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'
client = groq.Client(api_key=groq_api_key)

# Define a function to interact with Groq's LLM
def ask_groq(prompt, role="You are a helpful assistant.", model="mixtral-8x7b-32768"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Define roles for each agent
PROFESSOR_ROLE = "You are a Professor. Your role is to create comprehensive knowledge bases, explain concepts from first principles, and include key terminology."
ACADEMIC_ADVISOR_ROLE = "You are an Academic Advisor. Your role is to create detailed learning roadmaps, break topics into subtopics, and include time estimates."
RESEARCH_LIBRARIAN_ROLE = "You are a Research Librarian. Your role is to find quality learning resources, including books, articles, and online courses."
TEACHING_ASSISTANT_ROLE = "You are a Teaching Assistant. Your role is to create practice materials, including progressive exercises and real-world applications."

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle topic submission and generate responses
@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic')
    if not topic:
        return jsonify({'error': 'Please enter a topic.'}), 400

    # Generate responses from each agent
    professor_response = ask_groq(
        f"Create a comprehensive knowledge base on {topic}. Include key terminology and first principles.",
        role=PROFESSOR_ROLE
    )
    academic_advisor_response = ask_groq(
        f"Create a detailed learning roadmap for {topic}. Break it down into subtopics and include time estimates.",
        role=ACADEMIC_ADVISOR_ROLE
    )
    research_librarian_response = ask_groq(
        f"Find quality learning resources for {topic}. Include books, articles, and online courses.",
        role=RESEARCH_LIBRARIAN_ROLE
    )
    teaching_assistant_response = ask_groq(
        f"Create practice materials for {topic}. Include progressive exercises and real-world applications.",
        role=TEACHING_ASSISTANT_ROLE
    )

    # Return responses as JSON
    return jsonify({
        'professor': professor_response,
        'academic_advisor': academic_advisor_response,
        'research_librarian': research_librarian_response,
        'teaching_assistant': teaching_assistant_response
    })

if __name__ == '__main__':
    app.run(debug=True)
