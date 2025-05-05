#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <array>
#include <algorithm>
#include <iostream>


namespace py = pybind11;

int get_rank(int card) {
    return card % 13;
}

int get_suit(int card) {
    return card / 13;
}

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

int encode_score(HandRank rank, const std::vector<int>& key_cards, const std::vector<int>& kickers) {
    int score = (rank << 20);

    int shift = 16;
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

std::pair<int, std::string> evaluate_hand(const std::vector<int>& cards) {
    std::array<int, 13> rank_counts = {0};

    for (int card : cards) {
        int rank = get_rank(card);
        rank_counts[rank]++;
    }

    std::vector<std::pair<int, int>> freq_rank;
    for (int r = 0; r < 13; ++r) {
        if (rank_counts[r] > 0) {
            freq_rank.emplace_back(rank_counts[r], r);
        }
    }

    // Sort by count desc, then rank desc
    std::sort(freq_rank.begin(), freq_rank.end(), [](auto a, auto b) {
        if (a.first != b.first) return a.first > b.first;
        return a.second > b.second;
    });

    // Track suits
    std::array<int, 4> suit_counts = {0};
    std::array<std::vector<int>, 4> suit_cards;

    for (int card : cards) {
        int rank = get_rank(card);
        int suit = get_suit(card);
        suit_counts[suit]++;
        suit_cards[suit].push_back(rank);
    }

    // Detect Flush (and Straight Flush)
    for (int suit = 0; suit < 4; ++suit) {
        if (suit_counts[suit] >= 5) {
            std::vector<int> suited = suit_cards[suit];

            // Sort descending and remove duplicates
            std::sort(suited.begin(), suited.end(), std::greater<>());
            suited.erase(std::unique(suited.begin(), suited.end()), suited.end());

            // Straight Flush Check
            std::vector<bool> seen(14, false);
            for (int r : suited) {
                seen[r] = true;
                if (r == 12) seen[0] = true;  // Ace low
            }

            int in_a_row = 0;
            for (int i = 12; i >= 0; --i) {
                if (seen[i]) {
                    in_a_row++;
                    if (in_a_row >= 5) {
                        std::vector<int> sf = {i + 4, i + 3, i + 2, i + 1, i};
                        if (i + 4 == 12) {
                            return std::make_pair(encode_score(ROYAL_FLUSH, {12}, {}), rank_to_string(ROYAL_FLUSH));
                        }
                        return std::make_pair(encode_score(STRAIGHT_FLUSH, {i + 4}, {}), rank_to_string(STRAIGHT_FLUSH));
                    }
                } else {
                    in_a_row = 0;
                }
            }

            // Otherwise, regular flush
            std::vector<int> top5(suited.begin(), suited.begin() + 5);

            // Read out flush cards for debugging
            //std::cout << "Flush cards used for scoring: ";
            //for (int r : top5) std::cout << r << " ";
            //std::cout << std::endl;

            return std::make_pair(encode_score(FLUSH, {}, top5), rank_to_string(FLUSH));
        }
    }

    // Detect Straight (non-suited)
    std::vector<int> unique_ranks;
    for (int r = 0; r < 13; ++r) {
        if (rank_counts[r] > 0) {
            unique_ranks.push_back(r);
        }
    }

    // Add low-Ace for wheel straight
    if (rank_counts[12] > 0) {  // Ace present
        unique_ranks.push_back(0);
    }

    // Sort descending
    std::sort(unique_ranks.begin(), unique_ranks.end(), std::greater<>());
    unique_ranks.erase(std::unique(unique_ranks.begin(), unique_ranks.end()), unique_ranks.end());

    // Look for 5-in-a-row
    int in_a_row = 1;
    for (size_t i = 1; i < unique_ranks.size(); ++i) {
        if (unique_ranks[i] == unique_ranks[i - 1] - 1) {
            in_a_row++;
            if (in_a_row >= 5) {
                int high = unique_ranks[i - 4];  // Highest card of the straight
                std::vector<int> straight = {high, high - 1, high - 2, high - 3, high - 4};
                return std::make_pair(encode_score(STRAIGHT, {high}, {}), rank_to_string(STRAIGHT));
            }
        } else {
            in_a_row = 1;
        }
    }

    if (freq_rank[0].first == 4) {
        // Four of a Kind
        int quad_rank = freq_rank[0].second;
        std::vector<int> kickers;
        for (auto [count, rank] : freq_rank) {
            if (rank != quad_rank) {
                for (int i = 0; i < count; ++i) {
                    kickers.push_back(rank);
                }
            }
        }
        std::sort(kickers.rbegin(), kickers.rend());
        return std::make_pair(encode_score(FOUR_OF_A_KIND, {quad_rank}, kickers), rank_to_string(FOUR_OF_A_KIND));
    }

        if (freq_rank[0].first == 3) {
        int trips_rank = freq_rank[0].second;
        int pair_rank = -1;

        // Look for second pair or another trips to use as pair
        for (size_t i = 1; i < freq_rank.size(); ++i) {
            if (freq_rank[i].first >= 2) {
                pair_rank = freq_rank[i].second;
                break;
            }
        }

        if (pair_rank != -1) {
            return std::make_pair(
                encode_score(FULL_HOUSE, {trips_rank, pair_rank}, {}),
                rank_to_string(FULL_HOUSE)
            );
        }
    }

    if (freq_rank[0].first == 3) {
        // Three of a Kind
        int trips = freq_rank[0].second;
        std::vector<int> kickers;
        for (auto [count, rank] : freq_rank) {
            if (rank != trips) {
                for (int i = 0; i < count; ++i) {
                    kickers.push_back(rank);
                }
            }
        }
        std::sort(kickers.rbegin(), kickers.rend());
        return std::make_pair(encode_score(THREE_OF_A_KIND, {trips}, kickers), rank_to_string(THREE_OF_A_KIND));
    }

    if (freq_rank[0].first == 2 && freq_rank.size() >= 2 && freq_rank[1].first == 2) {
        // Two Pair
        int high_pair = freq_rank[0].second;
        int low_pair = freq_rank[1].second;
        std::vector<int> kickers;
        for (auto [count, rank] : freq_rank) {
            if (rank != high_pair && rank != low_pair) {
                for (int i = 0; i < count; ++i) {
                    kickers.push_back(rank);
                }
            }
        }
        std::sort(kickers.rbegin(), kickers.rend());
        return std::make_pair(encode_score(TWO_PAIR, {high_pair, low_pair}, kickers), rank_to_string(TWO_PAIR));
    }

    if (freq_rank[0].first == 2) {
        // One Pair
        int pair_rank = freq_rank[0].second;
        std::vector<int> kickers;
        for (auto [count, rank] : freq_rank) {
            if (rank != pair_rank) {
                for (int i = 0; i < count; ++i) {
                    kickers.push_back(rank);
                }
            }
        }
        std::sort(kickers.rbegin(), kickers.rend());
        return std::make_pair(encode_score(ONE_PAIR, {pair_rank}, kickers), rank_to_string(ONE_PAIR));
    }

    // High Card
    std::vector<int> all_ranks;
    for (auto [count, rank] : freq_rank) {
        for (int i = 0; i < count; ++i) {
            all_ranks.push_back(rank);
        }
    }
    std::sort(all_ranks.rbegin(), all_ranks.rend());
    return std::make_pair(encode_score(HIGH_CARD, {}, all_ranks), rank_to_string(HIGH_CARD));
}



// batch evaluation logic
std::vector<std::vector<int>> batch_evaluate(const std::vector<std::array<std::array<int, 7>, 6>>& games) {
    std::vector<std::vector<int>> results;
    results.reserve(games.size());

    for (const auto& game : games) {
        std::vector<std::pair<int, int>> scores; // (score, player index)

        for (int i = 0; i < 6; ++i) {
            int score = evaluate_hand(std::vector<int>(game[i].begin(), game[i].end())).first;
            scores.emplace_back(score, i);
        }

        // Find the max score
        int max_score = std::max_element(scores.begin(), scores.end())->first;

        std::vector<int> winners;
        for (const auto& [score, idx] : scores) {
            if (score == max_score) {
                winners.push_back(idx);
            }
        }

        results.push_back(winners);
    }

    return results;
}




PYBIND11_MODULE(hand_eval, m) {
    m.def("evaluate_hand", &evaluate_hand, "Evaluate a 7-card poker hand");
    m.def("batch_evaluate", &batch_evaluate, "Batch evaluate games to determine winners");
}