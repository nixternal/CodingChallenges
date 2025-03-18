package main

import (
  "fmt"
  "os"
  "regexp"
  "strconv"
  "strings"
)

// Read the input data from "input.txt" file. Parse the data into a string of
// the "memory dump" and return it.
func readPuzzleInput() string {
  file, err := os.ReadFile("../input.txt")
  if err != nil {
    panic(err)
  }

  memory := string(file)
  return memory
}

// Find all of the digits inside of a "mul()", ie mul(1,2) would give us [1,2].
// Return a list of all matches
func getMatches(memory string) [][]string {
  re := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
  return re.FindAllStringSubmatch(memory, -1)
}

// Get all of the "mul()" digits from "getMatches()" function, multiply each
// pair of digits and then add their products together. Return the sum of
// products.
func partOne(memory string) int {
  sum := 0
  matches := getMatches(memory)
  for _, match := range matches {
    a, err1 := strconv.Atoi(match[1])
    b, err2 := strconv.Atoi(match[2])
    if err1 != nil || err2 != nil {
      fmt.Println("Error converting to int:", err1, err2)
      continue
    }
    sum += a * b
  }
  return sum
}

// In part 2 of the puzzle we only sum the values of our digits if they follow
// a "do()" function in the corrupted memory dump.
func partTwo(memory string, enabled bool) int {
  if enabled {
    if strings.Contains(memory, "don't()") {
      i := strings.Index(memory, "don't")
      return partOne(memory[:i]) + partTwo(memory[i:], false)
    } else {
      return partOne(memory)
    }
  } else {
    if strings.Contains(memory, "do()") {
      i := strings.Index(memory, "do()")
      return partTwo(memory[i:], true)
    } else {
      return 0
    }
  }
}

// Orchestrate the program flow by calling the functions to print out the
// solved Part 1 and Part 2 functions of the puzzle.
func main() {
  fmt.Println("Part 1:", partOne(readPuzzleInput()))        // 174960292
  fmt.Println("Part 2:", partTwo(readPuzzleInput(), true))  // 56275602
}
