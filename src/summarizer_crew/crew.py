from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class SummarizerCrew():
    """BlogSummaryCrew handles link verification, content extraction, and summarization"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def content_fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config['content_fetcher'],
            tools=[SerperDevTool(
                search_url="site:{link}",
                n_results=1,
            )],
            verbose=True,
        )

    @agent
    def blog_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_summarizer'],
            verbose=True,
        )

    @agent
    def design_suggester(self) -> Agent:
        return Agent(
            config=self.agents_config['design_suggester'],
            verbose=True,
        )

    @task
    def fetch_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_content_task'],
            verbose=True,
        )

    @task
    def summarize_blog_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_blog_task'],
            output_file='summary.md'
        )

    @task
    def design_suggestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_suggestion_task'],
            output_file='summary.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
