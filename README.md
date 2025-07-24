# 🍝 Spaghetti Task Manager

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Workshop Material](https://img.shields.io/badge/workshop-material-orange.svg)](https://github.com/your-repo/spaghetti-task-manager)

> **A deliberately bad Python application designed for refactoring workshops using principles from "A Philosophy of Software Design"**

This repository contains a monolithic, single-file Python task manager that intentionally violates nearly every good design principle from John Ousterhout's *A Philosophy of Software Design*. Use it as a hands-on learning tool to practice identifying anti-patterns and applying better design principles.

## Table of Contents

- [Workshop Objectives](#-workshop-objectives)
- [Prerequisites](#-prerequisites)  
- [Quick Start](#-quick-start)
- [Anti-Patterns Demonstrated](#-anti-patterns-demonstrated)
- [Workshop Activities](#-workshop-activities)
- [Learning Outcomes](#-learning-outcomes)
- [Contributing](#-contributing)
- [License](#-license)

## Workshop Objectives

By the end of this workshop, participants will be able to:

- **Identify** common software design anti-patterns in real code
- **Apply** principles from "A Philosophy of Software Design" to improve code structure
- **Refactor** shallow modules into deep modules with clean interfaces
- **Eliminate** temporal decomposition and reduce unnecessary dependencies
- **Create** maintainable code through better abstraction and information hiding

## Prerequisites

### Required Knowledge
- Basic Python programming experience
- Understanding of object-oriented programming concepts
- Familiarity with version control (Git)

### Required Software
- Python 3.6 or higher
- Git
- Text editor or IDE of your choice
- Terminal/command line access

### Recommended Reading
- *A Philosophy of Software Design* by John Ousterhout (especially Chapters 4-6)
- Basic understanding of refactoring concepts

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/spaghetti-task-manager.git
cd spaghetti-task-manager
```

### 2. Create Your Working Branch
```bash
git checkout -b refactoring-workshop
```

### 3. Run the Application
```bash
python task_manager.py
```

### 4. Explore the Mess
Open `task_manager.py` and prepare to be horrified! 😱

## Anti-Patterns Demonstrated

This codebase is a carefully crafted disaster that demonstrates multiple design anti-patterns:

### **Shallow Module Design**
- **What**: The `TaskManager` class has dozens of trivial methods instead of hiding complexity behind a simple interface
- **Where**: Lines 25-120 in `task_manager.py`
- **Impact**: Interface complexity far exceeds functionality provided

### **Global State Chaos**
- **What**: Global variables (`TASKS`, `COMPLETED`, `SETTINGS`, `_conn`) scattered throughout
- **Where**: Lines 15-22
- **Impact**: Creates hidden dependencies and makes testing impossible

### **Spaghetti Control Flow**
- **What**: The `main()` function mixes UI logic, business logic, I/O, and database operations
- **Where**: Lines 180-250
- **Impact**: Violates single responsibility principle and creates cognitive overload

### **Temporal Decomposition**
- **What**: Logic split by *when* operations happen rather than *what* they do
- **Where**: `process_morning_tasks()`, `process_afternoon_tasks()`, `process_evening_tasks()`
- **Impact**: Related functionality scattered across multiple functions

### **Additional Anti-Patterns**
- **Inconsistent Naming**: `addTask()` vs `removeTask()` vs `complete_task()`
- **Side Effects Everywhere**: Direct `print` statements and `os.system` calls
- **Code Duplication**: Backup/restore logic repeated in multiple places  
- **Poor Error Handling**: Try-catch blocks that silently fail
- **Threading Misuse**: Unnecessary complexity in `fancy_spinner()`

## Workshop Activities

### 1: Code (15 minutes)
1. **Run the application** and understand what it does
2. **Read through the code** and identify the anti-patterns
3. **Document your findings** - what makes this code hard to understand?

### 2: Design (15 minutes)
1. **Sketch a better architecture** - how would you organize this code?
2. **Identify deep modules** - what functionality could be hidden behind simple interfaces?
3. **Plan your refactoring strategy** - what would you tackle first?

### 3: Refactor (25 minutes)
**Your challenge**: Transform this mess into well-designed code using principles from "A Philosophy of Software Design"

**Focus areas**:
- Create **deep modules** with simple interfaces and complex implementations
- Eliminate **temporal decomposition** by grouping related functionality
- Remove **global state** and create proper abstractions
- Establish clear **separation of concerns**

### 4: Review & Discuss (5 minutes)
- Share your refactoring approach with the group
- Discuss what you learned about software design
- Reflect on which anti-patterns were hardest to fix

## Learning Outcomes

After completing this workshop, you will have practical experience with:

| Concept | Before | After |
|---------|--------|-------|
| **Module Depth** | Shallow methods that do almost nothing | Deep modules that hide complexity |
| **Interface Design** | Complex, inconsistent interfaces | Simple, intuitive interfaces |
| **Code Organization** | Logic scattered by time/sequence | Logic grouped by functionality |
| **State Management** | Global variables everywhere | Encapsulated, controlled state |
| **Error Handling** | Silent failures and crashes | Robust error management |

## Extension Activities

Ready for more? Try these advanced challenges:

1. **Add Unit Tests** - How would you make this code testable?
2. **Implement Design Patterns** - Where would patterns like Strategy or Command help?
3. **Performance Analysis** - What are the performance implications of the original design?
4. **Scalability Review** - How would this code behave with 10,000 tasks?

## Contributing

Found a new anti-pattern to add? Want to improve the workshop experience?

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-anti-pattern`)
3. Make your changes
4. Add documentation explaining the anti-pattern
5. Submit a pull request

## Additional Resources

### Books
- **A Philosophy of Software Design** by John Ousterhout
- **Refactoring: Improving the Design of Existing Code** by Martin Fowler
- ~**Clean Code** by Robert C. Martin~

### Articles
- [Deep vs Shallow Modules](https://softengbook.org/articles/deep-modules)
- [The Nature of Software Complexity](https://web.stanford.edu/~ouster/cgi-bin/papers/complexity-cacm.pdf)

## Need Help?

- Check the **Issues** tab for common questions
- Review the **Wiki** for detailed explanations of each anti-pattern
- Join our **Discussions** to share your refactoring approaches

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Remember**: The goal isn't to create perfect code in one hour, but to practice recognizing anti-patterns and applying better design principles. Happy refactoring!

> *"The greatest enemy of good software design is complexity. Anything that makes software hard to understand or modify will ultimately lead to problems."* - John Ousterhout
