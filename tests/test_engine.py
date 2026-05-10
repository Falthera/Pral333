#!/usr/bin/env python3
"""
PRAL333 Engine Testing Framework
Tests engine compilation, correctness, and performance
"""

import subprocess
import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class TestResult:
    def __init__(self, name: str, passed: bool, message: str = "", time_ms: float = 0):
        self.name = name
        self.passed = passed
        self.message = message
        self.time_ms = time_ms

    def __str__(self):
        status = f"{GREEN}✓ PASS{RESET}" if self.passed else f"{RED}✗ FAIL{RESET}"
        time_str = f" ({self.time_ms:.1f}ms)" if self.time_ms > 0 else ""
        msg = f" - {self.message}" if self.message else ""
        return f"{status} {self.name}{time_str}{msg}"

class PralTester:
    def __init__(self, src_dir: str = "src", binary_name: str = "stockfish"):
        self.src_dir = Path(src_dir)
        self.binary_path = self.src_dir / binary_name
        self.results: List[TestResult] = []
        
    def compile(self) -> bool:
        """Compile the engine"""
        print(f"\n{BLUE}{BOLD}=== Compilation Test ==={RESET}")
        try:
            # Clean build
            result = subprocess.run(
                ["make", "clean"],
                cwd=self.src_dir,
                capture_output=True,
                timeout=30
            )
            
            # Compile
            result = subprocess.run(
                ["make", "-j4", "ARCH=x86-64-bmi2", "COMP=gcc"],
                cwd=self.src_dir,
                capture_output=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.results.append(TestResult("Compilation", True, "Engine built successfully"))
                return True
            else:
                stderr = result.stderr.decode('utf-8', errors='ignore')
                self.results.append(TestResult("Compilation", False, f"Build failed: {stderr[:100]}"))
                return False
        except subprocess.TimeoutExpired:
            self.results.append(TestResult("Compilation", False, "Build timeout"))
            return False
        except Exception as e:
            self.results.append(TestResult("Compilation", False, str(e)))
            return False

    def test_engine_starts(self) -> bool:
        """Test that engine starts and responds to UCI commands"""
        print(f"\n{BLUE}{BOLD}=== Engine Start Test ==={RESET}")
        try:
            proc = subprocess.Popen(
                [str(self.binary_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            # Send UCI command
            proc.stdin.write("uci\n")
            proc.stdin.flush()
            
            output = proc.stdout.readline()
            proc.terminate()
            
            if "id name" in output:
                self.results.append(TestResult("Engine Start", True, "Engine responds to UCI"))
                return True
            else:
                self.results.append(TestResult("Engine Start", False, "No UCI response"))
                return False
        except Exception as e:
            self.results.append(TestResult("Engine Start", False, str(e)))
            return False

    def test_initial_position(self) -> bool:
        """Test evaluation of initial position"""
        print(f"\n{BLUE}{BOLD}=== Initial Position Test ==={RESET}")
        try:
            proc = subprocess.Popen(
                [str(self.binary_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            commands = [
                "position startpos\n",
                "go depth 8\n"
            ]
            
            for cmd in commands:
                proc.stdin.write(cmd)
                proc.stdin.flush()
            
            output = ""
            start_time = time.time()
            while time.time() - start_time < 20:
                line = proc.stdout.readline()
                if not line:
                    break
                output += line
                if "bestmove" in line:
                    break
            
            proc.terminate()
            
            if "bestmove" in output:
                # Extract eval if possible
                self.results.append(TestResult("Initial Position Eval", True, "Engine evaluated position"))
                return True
            else:
                self.results.append(TestResult("Initial Position Eval", False, "No bestmove found"))
                return False
        except Exception as e:
            self.results.append(TestResult("Initial Position Eval", False, str(e)))
            return False

    def test_perft(self) -> bool:
        """Test perft on initial position (shallow depth)"""
        print(f"\n{BLUE}{BOLD}=== Perft Test ==={RESET}")
        try:
            proc = subprocess.Popen(
                [str(self.binary_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            # Perft at depth 5 should give 4,865,609 nodes
            proc.stdin.write("position startpos\n")
            proc.stdin.write("go perft 5\n")
            proc.stdin.flush()
            
            output = ""
            start_time = time.time()
            while time.time() - start_time < 25:
                line = proc.stdout.readline()
                if not line:
                    break
                output += line
                if "Nodes searched" in line:
                    break
            
            proc.terminate()
            
            # Expected: 4,865,609
            if "Nodes searched: 4865609" in output or "4865609" in output:
                self.results.append(TestResult("Perft (depth 5)", True, "Correct node count"))
                return True
            else:
                self.results.append(TestResult("Perft (depth 5)", False, "Incorrect perft result"))
                return False
        except Exception as e:
            self.results.append(TestResult("Perft (depth 5)", False, str(e)))
            return False

    def test_search_depth(self) -> bool:
        """Test search reaches expected depth"""
        print(f"\n{BLUE}{BOLD}=== Search Depth Test ==={RESET}")
        try:
            proc = subprocess.Popen(
                [str(self.binary_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            
            proc.stdin.write("position startpos\n")
            proc.stdin.write("go depth 20 movetime 5000\n")
            proc.stdin.flush()
            
            output = ""
            max_depth = 0
            start_time = time.time()
            while time.time() - start_time < 10:
                line = proc.stdout.readline()
                if not line:
                    break
                output += line
                if "info depth" in line:
                    try:
                        depth = int(line.split("depth ")[1].split()[0])
                        max_depth = max(max_depth, depth)
                    except:
                        pass
                if "bestmove" in line:
                    break
            
            proc.terminate()
            
            if max_depth >= 18:
                self.results.append(TestResult(f"Search Depth", True, f"Reached depth {max_depth}"))
                return True
            else:
                self.results.append(TestResult(f"Search Depth", False, f"Only reached depth {max_depth}"))
                return False
        except Exception as e:
            self.results.append(TestResult("Search Depth", False, str(e)))
            return False

    def benchmark(self) -> bool:
        """Run performance benchmark"""
        print(f"\n{BLUE}{BOLD}=== Benchmark Test ==={RESET}")
        try:
            proc = subprocess.Popen(
                [str(self.binary_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            proc.stdin.write("position startpos\n")
            proc.stdin.write("go depth 15 movetime 3000\n")
            proc.stdin.flush()
            
            nps_values = []
            start_time = time.time()
            while time.time() - start_time < 5:
                line = proc.stdout.readline()
                if not line:
                    break
                if "info" in line and "nps" in line:
                    try:
                        nps = int(line.split("nps ")[1].split()[0])
                        nps_values.append(nps)
                    except:
                        pass
                if "bestmove" in line:
                    break
            
            proc.terminate()
            
            if nps_values:
                avg_nps = sum(nps_values) / len(nps_values)
                self.results.append(TestResult("Benchmark", True, f"{avg_nps/1e6:.1f}M NPS"))
                return True
            else:
                self.results.append(TestResult("Benchmark", False, "Could not measure NPS"))
                return False
        except Exception as e:
            self.results.append(TestResult("Benchmark", False, str(e)))
            return False

    def print_summary(self):
        """Print test summary"""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print(f"\n{BLUE}{BOLD}{'='*60}")
        print(f"TEST SUMMARY: {passed}/{total} tests passed")
        print(f"{'='*60}{RESET}")
        
        for result in self.results:
            print(result)
        
        print()
        if passed == total:
            print(f"{GREEN}{BOLD}✓ ALL TESTS PASSED{RESET}")
            return True
        else:
            print(f"{RED}{BOLD}✗ {total - passed} TESTS FAILED{RESET}")
            return False

    def run_all(self) -> bool:
        """Run all tests"""
        print(f"{BOLD}{BLUE}PRAL333 Engine Test Suite{RESET}")
        print(f"Binary: {self.binary_path}\n")
        
        if not self.compile():
            print(f"{RED}Compilation failed, aborting tests{RESET}")
            self.print_summary()
            return False
        
        self.test_engine_starts()
        self.test_initial_position()
        self.test_perft()
        self.test_search_depth()
        self.benchmark()
        
        return self.print_summary()

if __name__ == "__main__":
    tester = PralTester()
    success = tester.run_all()
    sys.exit(0 if success else 1)
