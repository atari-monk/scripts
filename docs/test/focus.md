Here's a fun fictional test scenario that will help you test all the features of your focus script:

## 🎮 **The "Code Warrior's Quest" Scenario**

You're a programmer on a mission to build the ultimate gaming AI! Test your focus script by managing this epic coding journey.

### **Phase 1: Setting Up Your Quest**
```bash
# Create your main quest task list
focus create-list "AI_Dragon_Slayer" "Build an AI that can defeat the ancient code dragon"

# Add tasks to your quest
focus create-task "AI_Dragon_Slayer" "Research ancient dragon algorithms"
focus create-task "AI_Dragon_Slayer" "Design neural network architecture" 
focus create-task "AI_Dragon_Slayer" "Implement combat prediction system"
focus create-task "AI_Dragon_Slayer" "Train AI on historical battle data"
focus create-task "AI_Dragon_Slayer" "Test against dragon simulation"
focus create-task "AI_Dragon_Slayer" "Celebrate victory with virtual mead"
```

### **Phase 2: Starting Your Adventure**
```bash
# Begin your epic coding session!
focus start "AI_Dragon_Slayer"
# Output should show: "Current task: Research ancient dragon algorithms"

# Work for a bit, then move to next task
focus next
# Now you're designing neural network architecture!

# Oops! Dragon attack! You need to stop temporarily
focus stop
```

### **Phase 3: The Plot Thickens - Multiple Quests**
```bash
# Create a side quest for when you need a break
focus create-list "Magic_Potion_Brewing" "Create optimization algorithms (disguised as magic potions)"
focus create-task "Magic_Potion_Brewing" "Gather computational herbs"
focus create-task "Magic_Potion_Brewing" "Brew efficiency elixir"
focus create-task "Magic_Potion_Brewing" "Test on sample algorithms"

# Check your available quests
focus list
```

### **Phase 4: Resuming Your Main Quest**
```bash
# Resume where you left off (check the log name from 'focus list' first)
focus resume "AI_Dragon_Slayer" "AI_Dragon_Slayer_20241215_143022"

# Continue your work, moving through tasks
focus next  # Implement combat system
focus next  # Train AI
# ... imagine you're coding valiantly...
```

### **Phase 5: Managing Multiple Sessions**
```bash
# Try to start a new session while one is active (should fail gracefully)
focus start "Magic_Potion_Brewing"

# Stop current session properly
focus stop

# Now start the side quest
focus start "Magic_Potion_Brewing"
```

### **Phase 6: Checking Your Progress**
```bash
# See overall stats
focus stats

# Check specific quest progress
focus stats "AI_Dragon_Slayer"

# Get detailed battle report for a specific session
focus stats "AI_Dragon_Slayer" "AI_Dragon_Slayer_20241215_143022"
```

### **Phase 7: The Grand Finale**
```bash
# Complete all tasks in your main quest
focus resume "AI_Dragon_Slayer" "AI_Dragon_Slayer_20241215_143022"
focus next  # Complete final testing
focus next  # Should see "Session complete! All tasks finished."

# Check your victory stats!
focus stats "AI_Dragon_Slayer"
```

### **Phase 8: Data Management**
```bash
# Peek behind the curtain at your quest logs
focus file
# Choose to open either file and see the JSON structure
```

## 🏆 **What to Test For:**

1. **Error Handling**: Try starting a session that doesn't exist, or resuming with wrong names
2. **Data Persistence**: Stop Python, restart, and verify your sessions are still there
3. **Time Tracking**: Let some real time pass between start/stop to see minute calculations
4. **Edge Cases**: What happens when you try to go "next" on the last task?
5. **File Integrity**: Manually edit the JSON files and see if the script handles corrupt data gracefully

## 📊 **Expected Fun Outcomes:**

- Watch your total coding "quest time" accumulate
- See which "magic potions" (optimizations) you spend the most time on
- Track your progress toward slaying the "code dragon"
- Have a gamified way to stay focused on your actual coding tasks!

This scenario tests all your commands while making the testing process feel like an adventure. May your focus be sharp and your code compile on the first try! 🐉⚔️