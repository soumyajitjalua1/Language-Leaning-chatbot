# chatbot.py
import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import re

class LanguageLearningBot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = ChatOpenAI(
            temperature=0.7, 
            model_name="gpt-4",
            openai_api_key=self.api_key
        )
        self.memory = ConversationBufferMemory(return_messages=True)
        self.native_language = None
        self.learning_language = None
        self.proficiency_level = None
        self.current_mistakes = []
        self.session_id = None
        
    def setup_chain(self, scene):
        # Create a system prompt based on the user's language preferences and chosen scene
        system_prompt = f"""
        You are a helpful language tutor. The user is a {self.proficiency_level} level speaker of {self.learning_language} 
        and their native language is {self.native_language}.
        
        The conversation scene is: {scene}
        
        Please chat with the user in {self.learning_language}. Your task is to:
        1. Help them practice {self.learning_language} in a natural conversation
        2. Correct mistakes they make, but in a gentle way
        3. Use appropriate vocabulary for their {self.proficiency_level} level
        4. Start the conversation with a brief introduction and question in {self.learning_language}
        
        When you detect a mistake, format your response like this:
        "Your message here..."
        
        [Correction] You said "incorrect phrase" - it should be "correct phrase". This is because...
        
        Use [Correction] tag only when identifying mistakes.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        self.chain = ConversationChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            verbose=True
        )
        
    def analyze_response(self, bot_response):
        # Extract corrections using regex
        correction_pattern = r"\[Correction\] You said \"(.*?)\" - it should be \"(.*?)\"\. This is because(.*?)(?=\n|$)"
        matches = re.findall(correction_pattern, bot_response, re.DOTALL)
        
        for match in matches:
            mistake = match[0].strip()
            correction = match[1].strip()
            explanation = match[2].strip()
            
            # Determine mistake type (grammar, vocabulary, syntax, etc.)
            # This would need more sophisticated analysis in a real implementation
            if "grammar" in explanation.lower():
                mistake_type = "Grammar"
            elif "vocabulary" in explanation.lower() or "word" in explanation.lower():
                mistake_type = "Vocabulary"
            elif "pronunciation" in explanation.lower():
                mistake_type = "Pronunciation"
            elif "syntax" in explanation.lower() or "structure" in explanation.lower():
                mistake_type = "Syntax"
            else:
                mistake_type = "Other"
                
            self.current_mistakes.append({
                "mistake": mistake,
                "correction": correction,
                "type": mistake_type,
                "explanation": explanation
            })
            
            from database import record_mistake
            record_mistake(self.session_id, mistake, correction, mistake_type)
        
        return bot_response
        
    def generate_summary(self):
        if not self.current_mistakes:
            return "You did very well! I didn't notice any mistakes in your conversation."
        
        # Group mistakes by type
        mistakes_by_type = {}
        for mistake in self.current_mistakes:
            if mistake["type"] not in mistakes_by_type:
                mistakes_by_type[mistake["type"]] = []
            mistakes_by_type[mistake["type"]].append(mistake)
        
        summary = "Here's a summary of the mistakes you made during our conversation:\n\n"
        
        for mistake_type, mistakes in mistakes_by_type.items():
            summary += f"## {mistake_type} ({len(mistakes)})\n"
            for i, m in enumerate(mistakes, 1):
                summary += f"{i}. You said: \"{m['mistake']}\" → Correct: \"{m['correction']}\"\n"
            summary += "\n"
        
        # Generate improvement suggestions
        prompt = f"""
        The user is learning {self.learning_language} at a {self.proficiency_level} level.
        Here are the mistakes they made in our conversation:
        
        {summary}
        
        Based on these mistakes, provide 3-5 focused areas for improvement and specific
        exercises or resources they could use to work on these areas. Be specific and helpful.
        """
        
        improvement_suggestions = self.llm.predict(prompt)
        
        summary += "## Improvement Suggestions\n\n" + improvement_suggestions
        
        return summary
