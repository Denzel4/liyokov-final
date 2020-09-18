from flask import request
from project.server.handlers.database.agents import insert_agent, select_agent, update_agent, drop_agent


def save_agent():
    return insert_agent()

def get_agent():
    return select_agent(request.restful)

def modify_agent(agent_id):
    return update_agent(agent_id)

def delete_agent(agent_id):
    return drop_agent(agent_id)
