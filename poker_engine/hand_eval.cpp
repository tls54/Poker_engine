#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <array>
#include <algorithm>
#include <iostream>
#include <bitset>
#include <numeric>



namespace py = pybind11;

/*
Each card is represented by an integer between 0 and 51
This forms a 
*/ 

enum HandRank {
    HIGH_CARD = 1,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    ROYAL_FLUSH
};

std::string rank_to_string(HandRank rank) {
    switch (rank) {
        case HIGH_CARD: return "HIGH_CARD";
        case ONE_PAIR: return "ONE_PAIR";
        case TWO_PAIR: return "TWO_PAIR";
        case THREE_OF_A_KIND: return "THREE_OF_A_KIND";
        case STRAIGHT: return "STRAIGHT";
        case FLUSH: return "FLUSH";
        case FULL_HOUSE: return "FULL_HOUSE";
        case FOUR_OF_A_KIND: return "FOUR_OF_A_KIND";
        case STRAIGHT_FLUSH: return "STRAIGHT_FLUSH";
        case ROYAL_FLUSH: return "ROYAL_FLUSH";
        default: return "UNKNOWN";
    }
}
int get_rank(int card) {
    return card % 13;
}

int get_suit(int card) {
    return card / 13;
}

int encode_score(int primary_rank, int hand_rank, int kicker = 0, int kicker2 = 0) {
    return (primary_rank << 16) | (hand_rank << 8) | (kicker << 4) | kicker2;
}

int evaluate_hand(const std::array<int, 7>& cards) {
    std::array<int, 13> rank_count{};
    std::array<int, 4> suit_count{};
    std::array<std::bitset<13>, 4> suit_ranks{};
    std::bitset<13> rank_bits;

    for (int card : cards) {
        int rank = get_rank(card);
        int suit = get_suit(card);
        rank_count[rank]++;
        suit_count[suit]++;
        suit_ranks[suit].set(rank);
        rank_bits.set(rank);
    }

    // Ace-low straight support
    if (rank_bits.test(12)) rank_bits.set(0);

    // Check for flush and straight flush
    for (int suit = 0; suit < 4; ++suit) {
        if (suit_count[suit] >= 5) {
            std::bitset<13> flush_ranks = suit_ranks[suit];
            if (flush_ranks.test(12)) flush_ranks.set(0);
            for (int i = 12; i >= 4; --i) {
                if ((flush_ranks >> (i - 4)).to_ulong() & 0b11111) {
                    return encode_score(i, 8); // Straight flush
                }
            }
        }
    }

    // Four of a kind
    for (int i = 12; i >= 0; --i) {
        if (rank_count[i] == 4) {
            for (int j = 12; j >= 0; --j) {
                if (j != i && rank_count[j] > 0) {
                    return encode_score(i, 7, j);
                }
            }
        }
    }

    // Full house
    for (int i = 12; i >= 0; --i) {
        if (rank_count[i] >= 3) {
            for (int j = 12; j >= 0; --j) {
                if (j != i && rank_count[j] >= 2) {
                    return encode_score(i, 6, j);
                }
            }
        }
    }

    // Flush
    for (int suit = 0; suit < 4; ++suit) {
        if (suit_count[suit] >= 5) {
            std::bitset<13> flush_ranks = suit_ranks[suit];
            int count = 0, score = 0;
            for (int i = 12; i >= 0 && count < 5; --i) {
                if (flush_ranks.test(i)) {
                    score = (score << 4) | i;
                    count++;
                }
            }
            return encode_score(score, 5);
        }
    }

    // Straight
    for (int i = 12; i >= 4; --i) {
        if ((rank_bits >> (i - 4)).to_ulong() & 0b11111) {
            return encode_score(i, 4);
        }
    }

    // Three of a kind
    for (int i = 12; i >= 0; --i) {
        if (rank_count[i] == 3) {
            std::array<int, 2> kickers;
            int k = 0;
            for (int j = 12; j >= 0 && k < 2; --j) {
                if (j != i && rank_count[j] > 0) kickers[k++] = j;
            }
            return encode_score(i, 3, kickers[0], kickers[1]);
        }
    }

    // Two pair
    for (int i = 12; i >= 0; --i) {
        if (rank_count[i] >= 2) {
            for (int j = i - 1; j >= 0; --j) {
                if (rank_count[j] >= 2) {
                    for (int k = 12; k >= 0; --k) {
                        if (k != i && k != j && rank_count[k] > 0) {
                            return encode_score(i, 2, j, k);
                        }
                    }
                }
            }
        }
    }

    // One pair
    for (int i = 12; i >= 0; --i) {
        if (rank_count[i] >= 2) {
            std::array<int, 3> kickers;
            int k = 0;
            for (int j = 12; j >= 0 && k < 3; --j) {
                if (j != i && rank_count[j] > 0) kickers[k++] = j;
            }
            return encode_score(i, 1, kickers[0], (kickers[1] << 4) | kickers[2]);
        }
    }

    // High card
    int score = 0, count = 0;
    for (int i = 12; i >= 0 && count < 5; --i) {
        if (rank_count[i] > 0) {
            score = (score << 4) | i;
            count++;
        }
    }
    return encode_score(score, 0);
}

std::vector<int> batch_evaluate(const std::vector<std::array<int, 7>>& hands) {
    std::vector<int> results;
    results.reserve(hands.size());
    for (const auto& hand : hands) {
        results.push_back(evaluate_hand(hand));
    }
    return results;
}



PYBIND11_MODULE(hand_eval, m) {
    m.def("evaluate_hand", &evaluate_hand, "Evaluate a 7-card poker hand");
    m.def("batch_evaluate", &batch_evaluate, "Batch evaluate games to determine winners");
}