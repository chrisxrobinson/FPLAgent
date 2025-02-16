import logging
from . import data_processing
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, Graph
from typing import TypedDict, List
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AgentState(TypedDict):
    players: List[dict]
    team_analysis: dict
    constraints: dict
    recommendations: dict
    final_output: str

class AITransferAgent:
    """
    AITransferAgent integrates FPL analytics with LangChain and LangGraph to generate
    transfer suggestions and weekly performance reports.
    """
    def __init__(self, config=None):
        """
        Initializes the AITransferAgent.
        
        Parameters:
            config (dict, optional): Configuration options, e.g., API keys, thresholds.
                                    Defaults to an empty dictionary.
        """
        self.config = config or {}
        self.llm = ChatOpenAI(api_key=self.config.get("LLM_API_KEY"), temperature=0.7)
        
        transfer_prompt = PromptTemplate(
            input_variables=["players", "team_analysis", "constraints"],
            template=("Analyze the following player data: {players} and team performance: {team_analysis} "
                      "with constraints: {constraints} and suggest transfers with keys 'transfer_out' and 'transfer_in'.")
        )
        self.transfer_chain = LLMChain(llm=self.llm, prompt=transfer_prompt)
        
        weekly_prompt = PromptTemplate(
            input_variables=["players", "team_analysis"],
            template=("Generate a weekly report summary for the following player data: {players} "
                      "and team analysis: {team_analysis}.")
        )
        self.weekly_chain = LLMChain(llm=self.llm, prompt=weekly_prompt)
        
        self.graph = StateGraph(AgentState)
        
        self.graph.add_node("process_data", self._process_data)
        self.graph.add_node("analyze_transfers", self._analyze_transfers)
        self.graph.add_node("generate_recommendations", self._generate_recommendations)
        
        self.graph.add_edge('process_data', 'analyze_transfers')
        self.graph.add_edge('analyze_transfers', 'generate_recommendations')
        
        self.workflow: Graph = self.graph.compile()
        logger.info("AITransferAgent initialized with LangChain and LangGraph components.")

    def _process_data(self, state: AgentState) -> AgentState:
        """Process and prepare data for analysis"""
        player_df = data_processing.get_player_data()
        team_analysis = data_processing.analyze_team_performance()
        
        state['players'] = player_df.to_dict(orient="records")
        state['team_analysis'] = team_analysis
        return state

    def _analyze_transfers(self, state: AgentState) -> AgentState:
        """Analyze potential transfers using LangChain"""
        chain_input = {
            "players": state['players'],
            "team_analysis": state['team_analysis'],
            "constraints": state.get('constraints', {})
        }
        result = self.transfer_chain.run(chain_input)
        state['recommendations'] = json.loads(result) if isinstance(result, str) else result
        return state

    def _generate_recommendations(self, state: AgentState) -> AgentState:
        """Generate final recommendations"""
        recommendations = state['recommendations']
        summary = self.weekly_chain.run({
            "players": state['players'],
            "team_analysis": state['team_analysis']
        })
        state['final_output'] = {
            "transfers": recommendations,
            "summary": summary
        }
        return state

    def generate_transfer_suggestions(self):
        """
        Generates transfer suggestions using the LangGraph workflow
        """
        try:
            initial_state: AgentState = {
                "players": [],
                "team_analysis": {},
                "constraints": self.config.get("constraints", {}),
                "recommendations": {},
                "final_output": ""
            }
            
            result = self.workflow.invoke(initial_state)
            logger.info("Transfer suggestions generated successfully via LangGraph workflow.")
            return result["final_output"]
        except Exception as e:
            logger.error("Error in generate_transfer_suggestions: %s", e)
            raise

    def generate_weekly_report(self):
        """
        Generates a weekly report summarizing player and team performance.
        
        Optionally integrates a natural language summary using an LLM and includes suggestions
        for visualization (e.g., charts, graphs).
        
        Returns:
            dict: A dictionary containing the weekly performance report.
        """
        try:
            player_df = data_processing.get_player_data()
            team_analysis = data_processing.analyze_team_performance()
            
            chain_input = {
                "players": player_df.to_dict(orient="records"),
                "team_analysis": team_analysis
            }
            summary = self.weekly_chain.run(chain_input)
            
            report = {
                "player_report": player_df.head(5).to_dict(orient="records"),
                "team_analysis": team_analysis,
                "summary": summary,
                "visualization": "Chart placeholder URL/path if generated."
            }
            logger.info("Weekly report generated successfully via LangChain.")
            return report
        except Exception as e:
            logger.error("Error in generate_weekly_report: %s", e)
            raise

    def visualize_chain(self):
        """
        Visualizes the LangGraph workflow using the built-in visualization capabilities
        
        Returns:
            str: Path to the generated workflow visualization
        """
        try:
            visualization_path = "workflow_visualization.png"
            self.workflow.show().save(visualization_path)
            logger.info(f"Workflow visualization saved to {visualization_path}")
            return visualization_path
        except Exception as e:
            logger.error("Error visualizing workflow: %s", e)
            raise
