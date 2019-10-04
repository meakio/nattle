import click
import numpy as np


np.set_printoptions(threshold=np.inf, edgeitems=np.inf)


def clear():
    print(chr(27) + "[2J")


@click.command()
@click.option(
    "--width",
    prompt="Set width",
    type=click.IntRange(8, 25),
    default=10,
    help="Width of the naval battle [10, 50].",
)
@click.option(
    "--height",
    prompt="Set height",
    type=click.IntRange(8, 25),
    default=10,
    help="Height of the naval battle [10, 50].",
)
@click.option(
    "--ships",
    type=click.IntRange(1, 5),
    default=2,
    help="The number of ships.",
)
def cli(width, height, ships):
    clear()
    print(f"Begin of the naval battle [{width}, {height}]")
    print(f"Two players will place four ships on the board")

    players = [1, 2]
    seas = [Sea(width, height, ships, player) for player in players]

    for sea in seas:
        sea.set_ships()

    clear()

    game_continue = True
    while game_continue:
        for sea, player in zip(seas, players):
            x_limit = sea.width - 1
            position_x = click.prompt(
                f"Set the y-axis position of the shot [0, {x_limit}]",
                type=click.IntRange(0, x_limit),
            )

            y_limit = sea.height - 1
            position_y = click.prompt(
                f"Set the x-axis position of the shot [0, {y_limit}]",
                type=click.IntRange(0, y_limit),
            )

            print(position_x, position_y)

            all_player_loose = True
            for other_sea in seas:
                if other_sea == sea:
                    continue
                other_sea.shot((position_x, position_y), player)
                other_sea.print()
                if np.sum(other_sea.ship_alive) != 0:
                    all_player_loose = False

            if all_player_loose:
                print(f"Player {player} win")
                game_continue = False
                break

    for sea in seas:
        sea.print(with_ships=True)

    print(f"Come back to play again !")


class Sea(object):
    def __init__(self, width, height, n_ships, player):
        self.width = width
        self.height = height

        self.n_ships = n_ships

        self.player = player

        self.ship_sizes = [4] * self.n_ships
        self.ship_positions = []
        self.ship_alive = [True] * self.n_ships

        self.sea = np.zeros((self.width, self.height), np.int)

    def print(self, with_ships=False):
        print(f"Sea of player {self.player}")

        sea = np.copy(self.sea)

        if with_ships:
            ship_positions = set()
            for ship_position in self.ship_positions:
                for position in ship_position:
                    ship_positions.add(position)
            for position in ship_positions:
                sea[position] += 1

        print(sea)

    def shot(self, position, from_player):
        clear()

        self.sea[position] = -8

        ship_positions = set()
        for ship_position in self.ship_positions:
            for position in ship_position:
                ship_positions.add(position)

        if position in ship_positions:
            print(f"Player {from_player} touch a ship in position {position}")
            for ship, ship_position in enumerate(self.ship_positions):
                if position in set(ship_position):
                    dawn = 0
                    for index in ship_position:
                        if self.sea[index] < 0:
                            dawn += 1
                    if dawn == self.ship_sizes[ship]:
                        print("Ship {ship} is dawn")
                        self.ship_alive[ship] = False
                        if np.sum(self.ship_alive) == 0:
                            print("Player {self.player} lose")

        else:
            print(f"Player {from_player} don't touch in position {position}")


    def set_ships(self):
        clear()
        print(f"Player {self.player} place the ships")
        for ship in range(self.n_ships):
            size = self.ship_sizes[ship]

            direction = click.prompt(
                f"Set the direction of the {ship} ship (vertically: 0, horizontally: 1)",
                type=click.IntRange(0, 1),
            )

            if direction == 0:
                x_limit = self.height - 1
                y_limit = self.width - 1 - size
            else:
                x_limit = self.height - 1 - size
                y_limit = self.width - 1

            position_x = click.prompt(
                f"Set the y-axis position of the {ship} ship (size: {size}, [0, {x_limit}])",
                type=click.IntRange(0, x_limit),
            )
            position_y = click.prompt(
                f"Set the x-axis position of the {ship} ship (size: {size}, [0, {y_limit}])",
                type=click.IntRange(0, y_limit),
            )

            ship_position = []
            if direction == 0:
                for x in range(size):
                    ship_position.append((position_x + x, position_y))
            else:
                for y in range(size):
                    ship_position.append((position_x, position_y + y))
            self.ship_positions.append(ship_position)

            clear()
            self.print(with_ships=True)
