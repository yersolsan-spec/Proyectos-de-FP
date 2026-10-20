from __future__ import annotations

import random
import turtle


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
START_X = -320
FINISH_X = 300
LANE_HEIGHT = 80
LINE_EXTRA_HEIGHT = 30
MIN_VELOCITY = 1.85
MAX_VELOCITY = 7.0

COLOR_NAMES: dict[str, str] = {
    "red": "roja",
    "blue": "azul",
    "yellow": "amarilla",
    "green": "verde",
}

RUNNER_SPEEDS: dict[str, float] = {
    "blue": random.uniform(MIN_VELOCITY, MAX_VELOCITY),
    "red": random.uniform(MIN_VELOCITY, MAX_VELOCITY),
    "yellow": random.uniform(MIN_VELOCITY, MAX_VELOCITY),
    "green": random.uniform(MIN_VELOCITY, MAX_VELOCITY),
}


def prepare_screen() -> turtle.Screen:
    """Devuelve la pantalla de Turtle configurada para la carrera."""
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Circuit de la Torthue")
    return screen


def calculate_lane_positions(num_lanes: int) -> list[float]:
    """Calcula la coordenada Y para cada carril centrando la pista."""
    total_height = num_lanes * LANE_HEIGHT
    top_center = total_height / 2
    positions = []
    for i in range(num_lanes):
        lane = top_center - i * LANE_HEIGHT
        positions.append(lane)
    return positions


def draw_track(num_lanes: int) -> None:
    """Dibuja las líneas horizontales de la pista."""
    painter = turtle.Turtle(visible=False)
    painter.speed(0)
    painter.pensize(2)
    total_length = FINISH_X - START_X
    positions = calculate_lane_positions(num_lanes)
    for position in positions:
        painter.penup()
        painter.goto(START_X, position)
        painter.setheading(0)
        painter.pendown()
        painter.forward(total_length)


def draw_vertical_line(x_pos: float, top_y: float, bottom_y: float) -> None:
    """Dibuja una línea vertical roja entre las coordenadas dadas."""
    marker = turtle.Turtle(visible=False)
    marker.speed(0)
    marker.pensize(2)
    marker.color("red")
    marker.penup()
    marker.goto(x_pos, top_y)
    marker.setheading(270)
    marker.pendown()
    marker.forward(top_y - bottom_y)


def draw_start_line(num_lanes: int) -> None:
    """Marca la línea de salida."""
    positions = calculate_lane_positions(num_lanes)
    draw_vertical_line(
        START_X,
        positions[0] + LINE_EXTRA_HEIGHT,
        positions[-1] - LINE_EXTRA_HEIGHT,
    )


def draw_finish_line(num_lanes: int) -> None:
    """Marca la línea de llegada."""
    positions = calculate_lane_positions(num_lanes)
    draw_vertical_line(
        FINISH_X,
        positions[0] + LINE_EXTRA_HEIGHT,
        positions[-1] - LINE_EXTRA_HEIGHT,
    )


def setup_track(screen: turtle.Screen, num_lanes: int) -> None:
    """Dibuja la pista antes de colocar las tortugas."""
    screen.tracer(0)
    draw_track(num_lanes)
    draw_start_line(num_lanes)
    draw_finish_line(num_lanes)
    screen.tracer(1)


def create_runners(speed_map: dict[str, float]) -> list[tuple[turtle.Turtle, float]]:
    """Crea una tortuga por cada color y asocia su velocidad."""
    racers = []
    positions = calculate_lane_positions(len(speed_map))

    for i, (turtle_color, turtle_speed) in enumerate(speed_map.items()):
        runner = turtle.Turtle(shape="turtle")
        runner.color(turtle_color)
        runner.penup()
        runner.goto(START_X, positions[i])
        runner.setheading(0)
        racers.append((runner, turtle_speed))
    return racers


def invalid_speed_colors(speed_map: dict[str, float]) -> list[str]:
    """Devuelve los colores con velocidades iguales a cero o negativas."""
    return [color for color, speed in speed_map.items() if speed <= 0]


def spanish_color_list(colors: list[str]) -> str:
    """Convierte colores en una lista legible en español."""
    names = [COLOR_NAMES.get(color, color) for color in colors]
    if len(names) < 2:
        return "".join(names)
    if len(names) == 2:
        return " y ".join(names)
    return ", ".join(names[:-1]) + " y " + names[-1]


def announce_prediction(speed_map: dict[str, float]) -> None:
    """Explica antes de la carrera qué resultado predicen las velocidades."""
    print("Velocidades:")
    for color, speed in speed_map.items():
        print(f"  {COLOR_NAMES.get(color, color).capitalize()}: {speed:.2f}")

    fastest_speed = max(speed_map.values())
    fastest_colors = [
        color for color, speed in speed_map.items() if speed == fastest_speed
    ]
    if len(fastest_colors) > 1:
        names = spanish_color_list(fastest_colors)
        print(
            f"Predicción: empate entre {names}; comparten la velocidad máxima "
            f"({fastest_speed:.2f})."
        )
    else:
        name = COLOR_NAMES.get(fastest_colors[0], fastest_colors[0])
        print(
            f"Predicción: gana la {name}, porque su velocidad "
            f"({fastest_speed:.2f}) es la mayor."
        )


def show_invalid_speed_message(
    invalid_colors: list[str],
) -> None:
    """Muestra el aviso y cancela la carrera si hay velocidades no válidas."""
    names = spanish_color_list(invalid_colors)
    message = (
        "Aviso: todas las velocidades deben ser mayores que cero.\n"
        f"Carrera no iniciada. Revisa: {names}."
    )
    print(message)

    announcer = turtle.Turtle(visible=False)
    announcer.penup()
    announcer.color("red")
    announcer.goto(0, 0)
    announcer.write(message, align="center", font=("Arial", 16, "bold"))


def run_race(
    racers: list[tuple[turtle.Turtle, float]],
) -> list[turtle.Turtle]:
    """Anima la carrera y devuelve la tortuga o tortugas más rápidas."""
    fastest_speed = max(speed for _, speed in racers)
    winners = [runner for runner, speed in racers if speed == fastest_speed]

    # Todas salen del mismo punto, así que la velocidad máxima determina quién
    # llega antes. Las tortugas más rápidas con la misma velocidad llegan juntas.
    while any(runner.xcor() < FINISH_X for runner in winners):
        for runner, speed in racers:
            remaining_distance = FINISH_X - runner.xcor()
            if remaining_distance > 0:
                runner.forward(min(speed, remaining_distance))

    return winners


def show_winner_message(winners: list[turtle.Turtle]) -> None:
    """Anuncia la ganadora o el empate usando el color correspondiente."""
    announcer = turtle.Turtle(visible=False)
    announcer.penup()
    announcer.goto(0, -SCREEN_HEIGHT // 2 + 40)

    winner_colors = [runner.color()[0] for runner in winners]
    if len(winners) == 1:
        color = winner_colors[0]
        name = COLOR_NAMES.get(color, color)
        message = f"{name.capitalize()} más rápida: gana la {name}"
        announcer.color(color)
    else:
        names = spanish_color_list(winner_colors)
        message = f"¡Empate entre {names}! Tienen la misma velocidad máxima."
        announcer.color("black")

    announcer.write(message, align="center", font=("Arial", 16, "bold"))


def main() -> None:
    screen = prepare_screen()
    invalid_colors = invalid_speed_colors(RUNNER_SPEEDS)
    if invalid_colors:
        show_invalid_speed_message(invalid_colors)
        screen.mainloop()
        return

    announce_prediction(RUNNER_SPEEDS)
    number_of_runners = len(RUNNER_SPEEDS)
    setup_track(screen, number_of_runners)
    racers = create_runners(RUNNER_SPEEDS)
    winners = run_race(racers)
    show_winner_message(winners)
    screen.mainloop()


if __name__ == "__main__":
    main()
