package main

import (
  "bufio"
  "fmt"
  "math"
  "os"
  "sort"
  "strconv"
  "strings"
)

// Read the input data from "input.txt" file. Return 2 sorted slices: left &
// right. Ensure each line contains at least 2 integers, converted from
// strings. Invalid inputs are ignored, and mismatched lengths between left &
// right are reported.
func readPuzzleInput() ([]int, []int) {
  file, err := os.Open("../input.txt")
  if err != nil {
    panic(err)
  }
  defer file.Close()

  var left []int
  var right []int

  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    line:= scanner.Text()
    parts := strings.Fields(line)
    if len(parts) >= 2 {
      l, err := strconv.Atoi(parts[0])
      if err != nil {
        fmt.Println("Invalid input:", parts[0])
        continue
      }
      r, err := strconv.Atoi(parts[1])
      if err != nil {
        fmt.Println("Invalid input:", parts[1])
        continue
      }
      left = append(left, l)
      right = append(right, r)
    }
  }

  if err := scanner.Err(); err != nil {
    panic(err)
  }

  sort.Ints(left)
  sort.Ints(right)

  if len(left) != len(right) {
    fmt.Println("Mismatched lengths between left and right. Adjust input")
    return left, right
  }

  return left, right
}

// Compute the sum of absolute differences between corresponding elements in
// the sorted slices, left & right, and return the result.
func partOne(left[]int, right[]int) int {
  sum := 0
  for i := 0; i < len(left); i++ {
    sum += int(math.Abs(float64(left[i] - right[i])))
  }
  return sum
}

// Compute the weighted sum by multiplying each element in the left by its
// frequency in the right, using a frequency map for efficiency, and return the
// result.
func partTwo(left[]int, right[]int) int {
  freq := make(map[int]int)
  for _, val := range right {
    freq[val]++
  }
  sum := 0
  for _, l := range left {
    sum += l * freq[l]
  }
  return sum
}

// Orchestrate the program flow by calling the input reading function and
// solving Part 1 and Part 2 of the puzzle.
func main() {
  left, right := readPuzzleInput()
  fmt.Println("Part 1:", partOne(left, right))  // 1530215
  fmt.Println("Part 2:", partTwo(left, right))  // 26800609
}
