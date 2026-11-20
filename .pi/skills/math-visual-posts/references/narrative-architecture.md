# 数学题解：问题优先、推导透明、图形可核验

本文前半是 math-posts 的强制教学叙事；后半保留从 Colah / Annotated Transformer 借鉴的可视化组织方法。数学题不能直接套用论文叙事：读者首先需要知道题目对象、条件与目标。

## Mandatory math-post opening

每篇 HTML 在正式题干之前，必须出现一个独立的“先理解题目在问什么”区块。它至少说明：
1. 题目研究的对象是什么（函数、数列、几何体、点集、概率模型等）；
2. 已知条件限制了什么；
3. 题目最终要求什么；
4. 真正的难点或关键转化在哪里；
5. 一行解题路线：条件 → 模型 → 目标。

不能用 title、lead 或题干重述代替这一段。尤其是读者第一次见到“前 n 项积”“二阶周期点”“异面直线等距轨迹”等术语时，要先用直白语言解释其含义，再引入符号。

## Step-by-step explanation contract

每个 `<li>` 步骤都必须包含：
- **动作**：这一行具体做了什么；
- **依据**：来自哪个条件、定义、定理或等价变形；
- **解释**：为什么这一步能推进目标；
- **检查**：定义域、符号、单位、边界、等号或退化情况。

在每个步骤后增加一段本题专属的“为什么这样做”。避免空泛句式，例如“不要直接套公式”“把条件翻译成关系”。若出现“联立化简”“显然”“同理”“易得”，必须补出关键中间式或说明省略的只是简单算术。

解答题按小问组织；选择题逐项说明真伪依据；填空题要解释为什么唯一答案满足范围条件。

## Equation-to-figure map

每个关键公式应能在图中找到对应对象：变量对应点/长度/曲线，约束对应区域/边界，目标函数对应被绘制的量。图注写成可验证陈述，而不是“示意图”或“结构总览”。

例：若目标是前 n 项积 (P_n=a_1a_2\cdots a_n)，图中就画 (P_n) 的离散值；不能画通项 (a_n) 的递减曲线后再把它当成乘积的极值图。若图形只帮助直觉，必须明确标注“示意”，并在正文给出严格公式。

## The two complementary teaching moves

**Colah-style:** Start with a cognitive tension that the learner can feel, show one simple whole-object diagram, then unroll or highlight a reusable local idea. Move from a concrete example to the general rule and only then formalize. Use consistent labels and concise captions; do not overload the first figure.

**Annotated implementation:** Reorganize the explanation into dependencies. Explain a calculation alongside the geometric/algebraic object it represents, then test on a small numeric example, then return to the general statement. A visualization is an aid to reasoning, not a substitute for proof.

## Required story beats after the problem-first opening

1. **Question unpacking**: translate the task into ordinary language and name the unknown.
2. **Given / target map**: separate known conditions, domain restrictions and desired result.
3. **Key observation**: identify the property that unlocks the problem.
4. **Method choice**: explain why this method is suitable and what alternatives would miss.
5. **Stepwise derivation**: one transformation per step, with a reason and a local check.
6. **Equation with map**: explain each symbol and connect it to the figure.
7. **Visual or experiment**: show the actual mathematical object and a meaningful interaction only if useful.
8. **Answer and verification**: check units, boundary values, equality conditions and possible degeneracies.
9. **Transfer**: state which pattern can be reused and where it would fail.

## Figure storyboard

| Sequence | Question | Visual | Learner action |
|---|---|---|---|
| 1 | What object is moving/changing? | Geometry, curve, number-line or set diagram | identify variables |
| 2 | Which condition constrains it? | feasible region / interval / branch | locate boundary |
| 3 | What quantity is optimized or counted? | objective graph / discrete values / count tree | distinguish target from auxiliary quantity |
| 4 | Which transformation unlocks it? | before-and-after equations | follow the equivalence |
| 5 | Where does equality or a root occur? | marked point / intersection / endpoint | verify the result |

**Rule:** Write the mathematical assertion and its source before drawing. If the assertion, scale, labels or data do not match the derivation, the SVG is incorrect even if it looks polished.
