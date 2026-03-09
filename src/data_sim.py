import pandas as pd
import numpy as np
import time

def generate_raw_events(n=1000, p_legit=0.8, p_laggy=0.15, p_cheater=0.05):
    """
    Simulates raw telemetry events for players including spatial coordinates.
    """
    events = []
    types = ['legit', 'laggy', 'cheater']
    probabilities = [p_legit, p_laggy, p_cheater]
    
    # Store current state for each player to simulate movement
    player_states = {}

    for i in range(n):
        p_type = np.random.choice(types, p=probabilities)
        player_id = f"p_{np.random.randint(100, 999)}"
        
        if player_id not in player_states:
            player_states[player_id] = {
                'x': np.random.uniform(0, 1000),
                'y': np.random.uniform(0, 1000),
                'v': 5.0,
                'heading': np.random.uniform(0, 2 * np.pi)
            }
        
        state = player_states[player_id]
        
        # Base states and movement updates
        if p_type == 'legit':
            v, ping, loss = np.random.normal(5, 0.5), np.random.normal(30, 5), 0.1
            state['heading'] += np.random.normal(0, 0.1) # Smooth turns
        elif p_type == 'laggy':
            v, ping, loss = np.random.normal(20, 10), np.random.normal(400, 50), 5.0
            state['heading'] += np.random.normal(0, 0.5) # Erratic due to lag
        else: # cheater (aimbot/snap)
            v, ping, loss = np.random.normal(55, 2), np.random.normal(25, 5), 0.05
            # Sudden snap in direction
            if np.random.random() > 0.7:
                state['heading'] += np.random.uniform(np.pi/2, np.pi) 
            else:
                state['heading'] += np.random.normal(0, 0.05)
            
        # Update position based on velocity and heading
        state['x'] += v * np.cos(state['heading'])
        state['y'] += v * np.sin(state['heading'])
        state['v'] = v

        events.append({
            "player_id": player_id,
            "velocity": float(v),
            "ping": float(ping),
            "packet_loss": float(loss),
            "x": float(state['x']),
            "y": float(state['y']),
            "timestamp": time.time() + (i * 0.1), # Sequential timestamps
            "label": p_type
        })
    return events

if __name__ == "__main__":
    data = generate_raw_events(50)
    print(f"Generated {len(data)} sample events with spatial data.")
    print(data[0])
