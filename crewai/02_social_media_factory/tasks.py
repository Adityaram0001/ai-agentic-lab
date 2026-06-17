from crewai import Task
from agents import script_writer, thread_specialist, qa_reviewer

def get_tasks(raw_content: str):
    
    youtube_task = Task(
        description=f"Read the following article and write a 60-second YouTube Short script. It must include audio/visual cues.\n\nArticle:\n{raw_content}",
        expected_output="A formatted YouTube script with [Visual] and [Audio] tags.",
        agent=script_writer
    )
    
    twitter_task = Task(
        description=f"Read the following article and write a 5-part X/Twitter thread. Use emojis and bold text.\n\nArticle:\n{raw_content}",
        expected_output="A 5-post thread, clearly numbered 1/5, 2/5, etc.",
        agent=thread_specialist
    )
    
    qa_task = Task(
        description=f"Review BOTH the YouTube script and the Twitter thread. Compare them against the original article:\n\n{raw_content}\n\nFix ANY hallucinations (especially fake statistics) and output the final, corrected versions of both.",
        expected_output="The final, corrected YouTube script and Twitter thread, separated by a clear header.",
        agent=qa_reviewer,
        context=[youtube_task, twitter_task] # This makes the QA task explicitly depend on the outputs of the first two
    )
    
    return [youtube_task, twitter_task, qa_task]
