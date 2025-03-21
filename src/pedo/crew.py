from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pedo.tools.custom_tool import PdfReaderTool


@CrewBase
class Pedo():


    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

   
    @agent
    def reader_agent(self) -> Agent:
        pdfReaderTool = PdfReaderTool()
        return Agent(
            config=self.agents_config['reader_agent'],
            verbose=True,
            tools=[pdfReaderTool],
            memory=True,
        )

    @agent
    def text_processor(self) -> Agent:
        return Agent(
            config=self.agents_config['text_processor'],
            verbose=True
        )

    @agent
    def logo_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['logo_finder'],
            verbose=True
        )

    @agent
    def document_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['document_formatter'],
            verbose=True
        )
    
    
    
    @task
    def read_pdf_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_pdf_task'],
            outputs=["extracted_text"]
        )

    @task
    def text_processing_task(self) -> Task:
        return Task(
            config=self.tasks_config['text_processing_task'],
            inputs=["input_text"],  
            outputs=["structured_text"]  
        )

    @task
    def logo_fetching_task(self) -> Task:
        return Task(
            config=self.tasks_config['logo_fetching_task'],
        )

    @task
    def document_formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['document_formatting_task'],
            inputs=["structured_text"],  
        )


    @crew
    def crew(self) -> Crew:
        """Creates the PdfReader crew"""
      

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


    