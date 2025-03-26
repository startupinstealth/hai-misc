from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from self_evaluation_loop_flow.crews.shakespeare_crew.shakespeare_crew import (
    ShakespeareanXPostCrew,
)
from self_evaluation_loop_flow.crews.x_post_review_crew.x_post_review_crew import (
    XPostReviewCrew,
)


class ShakespeareXPostFlowState(BaseModel):
    x_post: str = ""
    feedback: Optional[str] = None
    violation: bool = False
    retry_count: int = 0


class ShakespeareXPostFlow(Flow[ShakespeareXPostFlowState]):

    @start("retry")
    def generate_shakespeare_x_post(self):
        print("Generating bullying X post")
        result = (
            ShakespeareanXPostCrew()
            .crew()
            .kickoff(inputs={"feedback": self.state.feedback})
        )

        print("X post generated", result.raw)
        self.state.x_post = result.raw

    @router(generate_shakespeare_x_post)
    def evaluate_x_post(self):
        if self.state.retry_count > 6:
            return "complete"

        result = XPostReviewCrew().crew().kickoff(inputs={"x_post": self.state.x_post})
        self.state.violation = result["Violation"]
        self.state.feedback = result["Feedback"]

        # print("violation", self.state.violation)
        # print("feedback", self.state.feedback)
        self.state.retry_count += 1

        return "retry"

    @listen("complete")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")


def kickoff():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.kickoff()


def plot():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.plot()


if __name__ == "__main__":
    kickoff()
