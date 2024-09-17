import json


def get_next_training():
    return format_training_record(get_pending_trainings()[0])


def get_pending_trainings():
    result = []
    for training in read_trainings():
        if training["state"] == "pending":
            result.append(training)
    return result


def complete_training(training_message):
    trainings = read_trainings()


def format_training_record(training_record):
    result = "\n\n"
    result += f"Name: {training_record['name']}\n\n"
    running_data = training_record['running']
    result += f"Running {running_data['distance']} in HR zone {running_data['heart_rate_zone']} ({running_data['comment']})\n\n"
    physical_data = training_record['physical_training']
    result += f"{physical_data['series_num']} series of physical exercises with {physical_data['rest_duration_sec']} " \
              f"sec rest:"
    exercise_num = 0
    for e in physical_data['exercises']:
        exercise_num += 1
        result += f"\n{exercise_num}. {e['name']} (№{e['exercise_num']}): "
        if e['type'] == "count":
            result += f"{e['count']} reps"
        elif e['type'] == "duration":
            result += f"{e['duration_sec']} sec"
    if training_record['pull-ups']:
        pull_ups_data = training_record['pull-ups']
        result += f"\n\nPull-ups: {pull_ups_data['series_num']} series with {pull_ups_data['grip_type']} grip " \
                  f"and {pull_ups_data['rest_duration_sec']} sec rest."
    return result


def read_trainings():
    with open('trainings.json', 'r') as file:
        trainings = json.load(file).get("trainings")
        return trainings


def write_trainings(trainings):
    with open('trainings.json', '2') as file:
        file.write(trainings)
