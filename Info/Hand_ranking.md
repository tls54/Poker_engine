# 🃏 Poker Hand Evaluation Scoring System (C++ Module)

This document explains how the C++ module evaluates 7-card poker hands and produces **comparable integer scores** that reflect the **relative strength** of each hand. Higher scores represent stronger hands.

---

## 🔢 Score Structure

The score is a **single integer** composed of:

$$
\text{SCORE} = (\text{HAND\_RANK} \ll 20) \mid (\text{KEY\_CARDS} \ll 4n) \mid (\text{KICKERS} \ll 4m)
$$

Where:
- $\text{HAND\_RANK}$ is an integer from 1 to 10 based on the poker hand category (e.g. `ONE_PAIR`, `FLUSH`, etc.)
- $\text{KEY\_CARDS}$ are the ranks that form the core of the hand (e.g. a pair of Kings → 13)
- $\text{KICKERS}$ are the remaining high cards used to break ties

Each rank is encoded using **4 bits** (i.e. values from 0 to 15).

---

## 🏆 Hand Rankings (Strength Order)

| Hand Type         | Enum Value | Shifted Left by 20 | Base Score |
|------------------|------------|--------------------|------------|
| Royal Flush       | 10         | $10 \ll 20$        | 10485760   |
| Straight Flush    | 9          | $9 \ll 20$         | 9437184    |
| Four of a Kind    | 8          | $8 \ll 20$         | 8388608    |
| Full House        | 7          | $7 \ll 20$         | 7340032    |
| Flush             | 6          | $6 \ll 20$         | 6291456    |
| Straight          | 5          | $5 \ll 20$         | 5242880    |
| Three of a Kind   | 4          | $4 \ll 20$         | 4194304    |
| Two Pair          | 3          | $3 \ll 20$         | 3145728    |
| One Pair          | 2          | $2 \ll 20$         | 2097152    |
| High Card         | 1          | $1 \ll 20$         | 1048576    |

All hands of a given type start from their **base score**, then additional values are added from the key cards and kickers to differentiate between hands of the same type.

---

## 🃏 Example: One Pair

```cpp
// Hand: One Pair of Aces with King, Queen, Jack kickers
// Encoded as:
score = (ONE_PAIR << 20)         // 2 << 20 = 2097152
      | (12 << 12)               // Pair of Aces (rank 12)
      | (11 << 8) | (10 << 4) | (9 << 0)  // KQJ kickers
```
Resulting score: 
$\text{score} = 2097152 + 49152 + 2816 + 160 + 9 = 2142089 $

## 🧠 Tie-Breaking

Since all components of the score are packed in decreasing significance:  
	1.	Hands of higher category always win (e.g. flush beats pair).  
	2.	Within the same category, the highest key_cards are compared.  
	3.	If still tied, kickers are compared from highest to lowest.  
	4.	Ties produce identical scores.  

You can directly use std::max() or sort players by their scores in Python to determine the winner(s).


## 🛠 How Scoring is Constructed in C++

The score is constructed via the encode_score(...) function:
```cpp
int encode_score(HandRank rank, const std::vector<int>& key_cards, const std::vector<int>& kickers) {
    int score = (rank << 20);   // Encodes hand strength
    int shift = 12;

    for (int k : key_cards) {
        score |= (k << shift);
        shift -= 4;
    }

    for (int k : kickers) {
        if (shift < 0) break;
        score |= (k << shift);
        shift -= 4;
    }

    return score;
}
```
The resulting score can be directly used for fast comparisons between hands.

## ✅ Summary
    •	All hand types are assigned increasing integer values for hierarchy.  
	•	key_cards and kickers help break ties.  ✅ Summary
	•	All hand types are assigned increasing integer values for hierarchy.
	•	key_cards and kickers help break ties.
	•	Scores are directly comparable — higher score = stronger hand.
	•	Python can sort or compare players based on these scores to determine winners, ties, or splits.
	•	Scores are directly comparable — higher score = stronger hand.
	•	Python can sort or compare players based on these scores to determine winners, ties, or splits.