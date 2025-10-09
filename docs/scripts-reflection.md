# Reflection on scripts

## BUILD A SIMPLE TOOL

1. Start with the absolute minimum that works
2. Add only essential features
3. Keep functions small and focused  
4. Make it easy to use daily
5. Don't over-engineer - build just what you need

I seen tool evolved from 100+ lines with complex classes
down to simple 25-line script that does the same job.

The journey from complex OOP architecture  
to a minimal script shows how we often overestimate what we need upfront.  
The simplest version that solves the core problem is usually the best starting point.

## Single file personal script

- Solves given tasks
- Complexity is proportional to task
- Minimizes count of lines, bug surface
- Maximizes functionality, readability, maintainability
- Dosent use hard to understand abstractions and patterns
- Argparse for cli features
- Type well so that no pylance errors, but use type where really needed 
- High code quality
- Test to break it
- Mesure if it is used 
