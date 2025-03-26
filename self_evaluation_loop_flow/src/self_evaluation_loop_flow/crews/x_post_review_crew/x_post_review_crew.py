from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from self_evaluation_loop_flow.tools.CharacterCounterTool import CharacterCounterTool


class XPostVerification(BaseModel):
    Violation: bool
    Feedback: Optional[str]


@CrewBase
class XPostReviewCrew:
    """X Post Review Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def x_post_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["x_post_verifier"]
        )

    @task
    def verify_x_post(self) -> Task:
        return Task(
            config=self.tasks_config["verify_x_post"],
            output_pydantic=XPostVerification,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the X Post Review Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
