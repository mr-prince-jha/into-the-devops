# 🤝 Contributing to Into The DevOps

Thank you for your interest in contributing to Into The DevOps! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Contribution Guidelines](#contribution-guidelines)
3. [Content Format](#content-format)
4. [Quality Standards](#quality-standards)
5. [Submission Process](#submission-process)
6. [Additional Resources](#additional-resources)

## 🚀 Getting Started

1. **Fork the Repository**
   - Click the 'Fork' button at the top right of this repository
   - Clone your fork locally: `git clone https://github.com/YOUR-USERNAME/into-the-devops.git`

2. **Create a Branch**
   - Create a new branch for your contribution:
     ```bash
     git checkout -b feature/your-contribution-name
     ```

3. **Set Up Development Environment**
   - Ensure you have Python installed for running validation scripts
   - Install any necessary dependencies (if applicable)

## 📝 Contribution Guidelines

### What We Accept

✅ **Do Contribute**:
- High-quality DevOps interview questions and answers
- Real-world scenarios and examples
- Best practices and common pitfalls
- Clear, concise explanations
- Practical exercises and solutions
- Updated or improved documentation

❌ **Don't Contribute**:
- Installation instructions or basic setup questions
- Content copied from other sources without permission
- Low-quality or unclear questions/answers
- Outdated technology references
- Non-free or copyrighted images

### Content Requirements

1. **Originality**
   - All content must be original or properly licensed
   - Give credit where due
   - Respect intellectual property rights

2. **Quality**
   - Content should be clear and well-explained
   - Include practical examples where possible
   - Ensure technical accuracy
   - Keep content up-to-date with current practices

3. **Relevance**
   - Content should be relevant to DevOps practices
   - Focus on practical, real-world scenarios
   - Target intermediate to advanced topics

## 📌 Content Format

### Question Format

Use the following format for adding questions:

```markdown
<details>
<summary>Your Question Here</summary><br><b>

Your detailed answer here. Make sure to:
- Use proper formatting
- Include code examples if applicable
- Add relevant diagrams or images if needed
- Provide references when necessary

</b></details>
```

### Formatting Guidelines

1. **Questions**
   - Should be clear and specific
   - Use proper grammar and punctuation
   - Avoid yes/no questions
   - Focus on practical scenarios

2. **Answers**
   - Provide comprehensive explanations
   - Include code examples when relevant
   - Use proper markdown formatting
   - Add diagrams or images if helpful

3. **Images**
   - Use only free-to-use images
   - Optimize images for web viewing
   - Include alt text for accessibility
   - Store in the appropriate images directory

## 🎯 Quality Standards

### Content Quality

1. **Technical Accuracy**
   - Ensure all technical information is correct
   - Verify code examples work
   - Test commands and procedures
   - Keep content up-to-date

2. **Writing Quality**
   - Use clear, professional language
   - Check grammar and spelling
   - Maintain consistent formatting
   - Follow markdown best practices

### Validation

1. **Local Testing**
   - Run the validation script before submitting:
     ```bash
     ./run_ci.sh
     ```
   - Fix any reported issues
   - Test all code examples

2. **Question Count**
   - Use the provided script to count questions:
     ```bash
     ./scripts/count_questions.sh
     ```

## 📤 Submission Process

1. **Before Submitting**
   - Run all validation scripts
   - Review your changes
   - Update documentation if needed
   - Test on your local environment

2. **Creating Pull Request**
   - Push your changes to your fork
   - Create a pull request from your branch
   - Fill out the PR template completely
   - Link any related issues

3. **PR Description**
   - Clearly describe your changes
   - Explain the motivation
   - List any dependencies
   - Mention related issues

## 🔍 Review Process

1. **Initial Check**
   - Automated tests will run
   - Basic formatting will be verified
   - Content guidelines will be checked

2. **Manual Review**
   - A maintainer will review your PR
   - Feedback may be provided
   - Changes may be requested
   - Discussions may occur in PR comments

## 📚 Additional Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [DevOps Best Practices](https://github.com/NotHarshhaa/into-the-devops)
- [Git Workflow Guide](https://guides.github.com/introduction/flow/)

## ❓ Questions or Problems?

If you have questions or run into problems:
- Open an issue in the repository
- Ask in the PR comments
- Join our [community chat](https://t.me/prodevopsguy)

---

Thank you for contributing to Into The DevOps! Your efforts help make this resource better for everyone in the DevOps community. 🙏
