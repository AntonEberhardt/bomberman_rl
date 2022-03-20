def setup(self):
    pass
    
def act(agent, game_state: dict):
    agent.logger.info('Places a bomb')
    return 'BOMB'
