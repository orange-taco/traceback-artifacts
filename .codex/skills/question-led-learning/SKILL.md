---
name: question-led-learning
description: Structure or review beginner learning artifacts as a progression of concrete questions from definition and category to integration form, responsibility, and practical variants. Use for unfamiliar technical concepts; do not force the full sequence when a question is irrelevant to the concept or the requested scope.
---

# Question-led Learning

Make the learner's next natural question determine the order of the explanation. Answer the small boundary questions before presenting detailed internals.

## Question ladder

Use this sequence when it fits the concept:

1. **What is it? — definition.** Give a plain-language definition and say what the term does not mean when ambiguity is likely.
2. **Where does it belong? — category.** Show the containing system, peers, and boundary. Do not imply that one product's architecture is universal.
3. **How does it exist or connect? — physical integration form.** Make the observable form clear: library, plugin, process, service, file format, protocol, or another real form. Show who calls whom. If the question is not meaningful for the concept, omit it.
4. **What does it do? — logical responsibility.** Follow one concrete input through the responsible actors to its output. Separate interface, orchestration, data access, persistence, and operating-system work when those owners differ.
5. **What kinds are used? — practical classification.** Group real examples by role or implementation, then explain only the representative variants needed by the requested scope.

The order is a default learning path, not a mandatory five-section template. Merge adjacent answers when that reduces repetition. Reorder only when the learner must observe something before the definition makes sense.

## Build or revise an artifact

- Start with the smallest example that can continue through the page. Reuse it instead of introducing disconnected examples.
- Put the short answer before the diagram or detail it unlocks. Define a difficult term at first use; move optional mechanisms into a collapsed detail.
- Label general principles and product-specific behavior visibly. Name the product and version for implementation claims.
- Prefer a visual that exposes containment, actors, input → processing → output, or before/after state. A row of decorative boxes is not evidence of a flow.
- Split foundational questions from implementation catalogs when depth would cause repetition. Link forward; do not copy the same explanation into both pages.
- Preserve the user's existing structure and interaction unless changing them is part of the request.

## Audit checklist

For an existing learning path, record each applicable question as **answered**, **partial**, or **missing** and point to the page or section that answers it. Then fix only gaps that affect the learning objective.

Check that:

- the first screen establishes the concept and scope before internals;
- category and physical form are not conflated;
- every major action has a named owner;
- the output of one step becomes the next step's input where a process is taught;
- examples do not mix unlike products under one unlabeled term;
- the practical taxonomy leads to representative depth rather than equal detail for every item;
- overview and deep-dive pages do not repeat the same explanation.
