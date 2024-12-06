package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
)

type Coord struct {
	x int
	y int
}
type Visits = map[Coord][]Coord

var DIRS = [...]Coord{
	{-1, 0},
	{0, 1},
	{1, 0},
	{0, -1},
}

func (c Coord) move(other Coord) Coord {
	return Coord{c.x + other.x, c.y + other.y}
}

func traverse(field [][]bool, start_position Coord) (Visits, error) {
	visits := make(Visits)
	direction := 0
	position := start_position
	rows_count := len(field)
	cols_count := len(field[0])

	for {
		visits[position] = append(visits[position], DIRS[direction])
		newPos := position.move(DIRS[direction])
		if newPos.x < 0 || newPos.y < 0 || newPos.x >= rows_count || newPos.y >= cols_count {
			return visits, nil
		}
		if field[newPos.x][newPos.y] {
			direction = (direction + 1) % len(DIRS)
			continue
		}
		if slices.Contains(visits[newPos], DIRS[direction]) {
			return nil, fmt.Errorf("loop detected")
		}
		position = newPos
	}
}
func main() {
	field := [][]bool{}
	startPosition := Coord{-1, -1}

	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	x := -1
	for scanner.Scan() {
		line := scanner.Text()
		x++
		row := make([]bool, 0, len(line))
		for y, ch := range line {
			if ch == '^' {
				startPosition = Coord{x, y}
			}
			row = append(row, ch == '#')
		}
		field = append(field, row)
	}

	visits, err := traverse(field, startPosition)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Result 1: %d \n", len(visits))

	obstacles := 0
	for cell := range visits {
		field[cell.x][cell.y] = true
		_, err = traverse(field, startPosition)
		if err != nil {
			obstacles += 1
		}
		field[cell.x][cell.y] = false
	}
	fmt.Printf("Result 2: %d \n", obstacles)
}
