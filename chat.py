from api import load_system_message
from api import chat_completion
from api import stringify_history


def main():
    stream = True
    verbose = False
    welcome_message = "Introduce yourself to someone opening this program for the first time. Be concise."
    system_message = load_system_message()
    history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": welcome_message},
    ]

    while True:
        new_message = {"role": "assistant", "content": ""}
        completion = chat_completion(stream, history)
        if stream:
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    new_message["content"] += chunk.choices[0].delta.content
            print()
        else:
            response = completion.choices[0].message.content
            print(response)
            new_message["content"] = response

        history.append(new_message)

        # print history if in verbose mode
        if verbose: print(stringify_history(history))
        else: print()

        q = input("> ")
        if q.lower() in [':q', ':x', ':quit', ':exit', 'bye']: break
        history.append({"role": "user", "content": q})


if __name__ == "__main__":
    main()
