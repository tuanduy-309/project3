from http import client
import tkinter as tk
from neo4j import GraphDatabase
from openai import OpenAI

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__password = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


def get_cypher_query(question):
    client = OpenAI(api_key='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')
    try:
        response = client.completions.create(
            model="text-davinci-003",
            prompt=f"Translate this natural language question into a Cypher query: '{question}'",
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
# query = "MATCH (n) RETURN n LIMIT 5"
# nodes = conn.query(query)
# for node in nodes:
#     print(node)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Neo4j App")

        self.conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

       
        self.label = tk.Label(root, text="Enter your question:")
        self.label.pack()

        self.question_entry = tk.Entry(root, width=50)
        self.question_entry.pack()

        self.run_button = tk.Button(root, text="OK", command=self.run_query)
        self.run_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def run_query(self):
        question = self.question_entry.get()
        cypher_query = get_cypher_query(question)
        print(cypher_query)
        if cypher_query:
            try:
                results = self.conn.query(cypher_query)
                values = []
                for record in results:
                    _str = str(record)
                    parts = _str.split("=")
                    result = parts[1].strip(">")
                    values.append(result)


                display_text = "\n".join(values)
                self.result_label.config(text=display_text)
            except Exception as e:
                self.result_label.config(text="Error: " + str(e))
        else:
            self.result_label.config(text="Failed to generate Cypher query.")

    def on_closing(self):
        self.conn.close()
        self.root.destroy()
        
root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()