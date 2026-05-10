/*
  Stockfish, a UCI chess playing engine derived from Glaurung 2.1
  Copyright (C) 2004-2026 The Stockfish developers (see AUTHORS file)

  Stockfish is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Stockfish is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "evaluate.h"

#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>

#include "nnue/network.h"
#include "nnue/nnue_misc.h"
#include "position.h"
#include "search.h"
#include "types.h"
#include "uci.h"
#include "nnue/nnue_accumulator.h"

namespace Stockfish {

// Evaluate is the evaluator for the outer world. It returns a static evaluation
// of the position from the point of view of the side to move.
Value Eval::evaluate(const Eval::NNUE::Network&     network,
                     const Position&                pos,
                     Eval::NNUE::AccumulatorStack&  accumulators,
                     Eval::NNUE::AccumulatorCaches& caches,
                     int                            optimism) {

    assert(!pos.checkers());

    auto [psqt, positional] = network.evaluate(pos, accumulators, caches);

    // PRAL333 Enhancement: Stronger NNUE blending with optimized coefficients
    Value nnue = (128 * psqt + 136 * positional) / 128;

    // Enhanced complexity evaluation for better position understanding
    int nnueComplexity = std::abs(psqt - positional);
    optimism += optimism * nnueComplexity / 412;  // Increased from 476
    nnue -= nnue * nnueComplexity / 15728;        // Reduced dampening from 18236

    // Aggressive material-based evaluation scaling
    int material = 534 * pos.count<PAWN>() + pos.non_pawn_material();
    int v        = (nnue * (68421 + material) + optimism * (9847 + material)) / 68421;  // Enhanced coefficients

    // Strengthened aggressive play bonus
    if (Search::ultra_aggressive())
    {
        const int attack = Search::attack_pressure(pos, pos.side_to_move());
        const int scale   = std::clamp(material / 1050, 0, 4);  // More aggressive scaling
        v += attack * scale / 2;  // Increased bonus from /3
    }

    // PRAL333: Enhanced position-specific evaluations
    // King safety bonus in endgames
    if (material < 3000) {
        const Square ourKing = pos.square<KING>(pos.side_to_move());
        const Bitboard safeSq = Search::king_ring(ourKing) & ~pos.attacks_by<KING>(~pos.side_to_move());
        v += __builtin_popcountll(safeSq) * 45;
    }
    
    // Passed pawn bonus enhancement
    Bitboard passed = pos.pieces(pos.side_to_move(), PAWN) & ~pos.attacks_by<PAWN>(~pos.side_to_move());
    v += __builtin_popcountll(passed) * 287;
    
    // Tempo bonus for aggressive positions
    if (nnueComplexity > 200) {
        v += 58;  // Reward complex positions where we move first
    }

    // Refined shuffling dampening with adaptive penalty
    int r50 = pos.rule50_count();
    if (r50 > 80) {
        v -= v * (r50 - 80) / 238;  // Stronger dampening in endgames
    } else {
        v -= v * r50 / 399;  // Original dampening from 199
    }

    // Guarantee evaluation does not hit the tablebase range
    v = std::clamp(v, VALUE_TB_LOSS_IN_MAX_PLY + 1, VALUE_TB_WIN_IN_MAX_PLY - 1);

    return v;
}

// Like evaluate(), but instead of returning a value, it returns
// a string (suitable for outputting to stdout) that contains the detailed
// descriptions and values of each evaluation term. Useful for debugging.
// Trace scores are from white's point of view
std::string Eval::trace(Position& pos, const Eval::NNUE::Network& network) {

    if (pos.checkers())
        return "Final evaluation: none (in check)";

    auto accumulators = std::make_unique<Eval::NNUE::AccumulatorStack>();
    auto caches       = std::make_unique<Eval::NNUE::AccumulatorCaches>(network);

    std::stringstream ss;
    ss << std::showpoint << std::noshowpos << std::fixed << std::setprecision(2);
    ss << '\n' << NNUE::trace(pos, network, *caches) << '\n';

    ss << std::showpoint << std::showpos << std::fixed << std::setprecision(2) << std::setw(15);

    auto [psqt, positional] = network.evaluate(pos, *accumulators, *caches);
    Value v                 = psqt + positional;
    ss << "NNUE evaluation          " << v << " (side to move, internal units)\n";
    v = pos.side_to_move() == WHITE ? v : -v;
    ss << "NNUE evaluation        " << 0.01 * UCIEngine::to_cp(v, pos) << " (white side)\n";

    v = evaluate(network, pos, *accumulators, *caches, VALUE_ZERO);
    v = pos.side_to_move() == WHITE ? v : -v;

    ss << "Final evaluation      ";
    ss << 0.01 * UCIEngine::to_cp(v, pos) << " (white side)";
    ss << " [with scaled NNUE, ...]\n";

    return ss.str();
}

}  // namespace Stockfish
