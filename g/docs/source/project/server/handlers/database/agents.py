from flask import request
from project.server.managers.database import db
from project.server.models.ai_agent import Agent
from project.server.helpers import database

def insert_agent():
    post_data = request.get_json()
    db.session.bulk_insert_mappings(Agent, post_data)
    db.session.commit()

def select_agent(restful):
    query = Agent.query.filter_by(**restful.filters)
    query = database.full_text_search(query, restful.q, [Agent.area])
    query = query.order_by(*database.get_order_by(Agent, restful.order_by))
    return database.get_list(query, restful.pagination)

def update_agent(agent_id):
    data = request.get_json()
    db.session.query(Agent).filter_by(id=agent_id).update(data)
    db.session.commit()

def drop_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()

