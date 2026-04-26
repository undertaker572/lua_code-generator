import os

from app.agents import AgentNetwork


def test_pipeline_returns_lua_and_report():
    os.environ["MOCK_LLM"] = "1"
    network = AgentNetwork(max_refinement_loops=1)
    result = network.run("Write Lua function that greets a name and print output.", language="en")

    assert "function" in result["final_lua"]
    assert isinstance(result["validation_report"], str)
    assert len(result["validation_report"]) > 0
