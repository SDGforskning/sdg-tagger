"""
Code to validate the logic rules of the SDGs (phrases) and country searches
"""
import re

TOKEN_REGEX = re.compile(
    r"""
    (?P<WS>\s+)                 |  # whitespace (nå BEHOLDER vi disse)
    \[(?P<IDENT>[a-z0-9_]+)\]   |  # [identifier] (små bokstaver, tall, underscore)
    (?P<LPAREN>\()              |  # (
    (?P<RPAREN>\))              |  # )
    (?P<NOT>\bnot\b)            |  # 'not' som eget ord
    (?P<AND>&)                  |  # &
    (?P<OR>\|)                     # |
    """,
    re.VERBOSE,
)

class Token:
    def __init__(self, kind, value=None, text="", start=0, end=0):
        self.kind = kind      # WS, IDENT, LPAREN, RPAREN, NOT, AND, OR
        self.value = value    # ident-navn for IDENT, ellers None
        self.text = text      # original tekst for token
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Token({self.kind!r}, {self.value!r}, {self.text!r})"


def tokenize(s: str):
    """Tokeniserer og sikrer at ingen ulovlige tegn finnes."""
    pos = 0
    tokens = []
    while pos < len(s):
        m = TOKEN_REGEX.match(s, pos)
        if not m:
            raise ValueError(f"Ugyldig tegn ved posisjon {pos}: {s[pos:pos+20]!r}")
        kind = m.lastgroup
        text = m.group(0)
        start, end = m.start(), m.end()

        if kind == "IDENT":
            tokens.append(Token("IDENT", m.group("IDENT"), text, start, end))
        elif kind == "WS":
            tokens.append(Token("WS", None, text, start, end))
        elif kind == "LPAREN":
            tokens.append(Token("LPAREN", None, text, start, end))
        elif kind == "RPAREN":
            tokens.append(Token("RPAREN", None, text, start, end))
        elif kind == "NOT":
            tokens.append(Token("NOT", None, text, start, end))
        elif kind == "AND":
            tokens.append(Token("AND", None, text, start, end))
        elif kind == "OR":
            tokens.append(Token("OR", None, text, start, end))
        else:
            raise ValueError(f"Uventet token: {text!r}")
        pos = end
    return tokens


def require_space_around_operator(tokens, i) -> None:
    """
    Krever minst ett whitespace-token både før og etter operator-token på indeks i.
    Kaster ValueError hvis kravet ikke oppfylles.
    """
    if i - 1 < 0 or i + 1 >= len(tokens):
        raise ValueError("Operator kan ikke stå først eller sist og må ha mellomrom på begge sider.")
    left = tokens[i - 1]
    right = tokens[i + 1]
    if left.kind != "WS" or len(left.text) < 1:
        raise ValueError("Mangler mellomrom før operator.")
    if right.kind != "WS" or len(right.text) < 1:
        raise ValueError("Mangler mellomrom etter operator.")


class Parser:
    """
    Grammatikk:

      EXPR  := TERM ( WS (AND|OR) WS TERM )*
      TERM  := ( WS NOT WS )? ( IDENT | LPAREN EXPR RPAREN )

    I tillegg håndhever vi:
      - Operatører må ha whitespace på begge sider (NOT, AND, OR).
      - LPAREN/RPAREN kan ha valgfri whitespace rundt (dette er ikke påkrevd).
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def consume(self, kind=None):
        t = self.peek()
        if t is None:
            return None
        if kind and t.kind != kind:
            raise ValueError(f"Forventet {kind}, men fant {t.kind}")
        self.i += 1
        return t

    def optionally_consume_ws(self):
        while self.peek() is not None and self.peek().kind == "WS":
            self.consume("WS")

    def parse_expr(self):
        # EXPR := TERM ( WS (AND|OR) WS TERM )*
        self.parse_term()
        while True:
            # Må ha minst ett WS før binær operator
            if self.peek() is None or self.peek().kind != "WS":
                break
            # Sjekk det ER en binær operator etter WS
            save_i = self.i
            self.optionally_consume_ws()
            t = self.peek()
            if t and t.kind in ("AND", "OR"):
                # Håndhev mellomrom før og etter (& og |)
                # Her vet vi at det var minst en WS før (fra blokken over)
                op_index = self.i
                # Konsumer operator
                self.consume()
                # Må ha minst ett WS etter
                if not self.peek() or self.peek().kind != "WS":
                    raise ValueError("Mangler mellomrom etter operator.")
                self.consume("WS")
                # Fortsett med TERM
                self.parse_term()
            else:
                # Ikke en operator—tilbakestill og avslutt EXPR
                self.i = save_i
                break

    def parse_term(self):
        # Tillat ledende whitespace
        self.optionally_consume_ws()

        # Håndter én eller flere 'not' med påkrevd mellomrom før og etter
        # Eksempel gyldig: " WS not WS [x] ", " WS not WS not WS ( ... ) "
        while True:
            t = self.peek()
            if t and t.kind == 'NOT':
                # Sjekk at det var minst ett whitespace rett før 'not'
                if self.i - 1 < 0 or self.tokens[self.i - 1].kind != 'WS':
                    raise ValueError("Operatoren 'not' må ha mellomrom før og etter.")
                # Konsumer 'not'
                self.consume('NOT')
                # Sjekk og konsumer minst ett whitespace etter 'not'
                if not self.peek() or self.peek().kind != 'WS':
                    raise ValueError("Operatoren 'not' må ha mellomrom etter.")
                self.consume('WS')
                # Tillat kjeding av flere 'not'
                # Fortsetter loopen hvis neste token også er 'NOT'
                continue
            break

        # Valgfri whitespace før faktoren
        self.optionally_consume_ws()

        # Faktor: IDENT eller '(' EXPR ')'
        t = self.peek()
        if t is None:
            raise ValueError("Uventet slutt: mangler identifikator eller parentessubuttrykk")

        if t.kind == 'IDENT':
            self.consume('IDENT')
        elif t.kind == 'LPAREN':
            self.consume('LPAREN')
            self.parse_expr()
            self.optionally_consume_ws()
            if not self.peek() or self.peek().kind != 'RPAREN':
                raise ValueError("Manglende avsluttende ')'")
            self.consume('RPAREN')
        else:
            raise ValueError(f"Forventet IDENT eller '(', men fant {t.kind}")

    def at_end(self):
        return self.i == len(self.tokens)


def validate_boolean_expression(s: str) -> bool:
    """
    Validerer:
      - Hele strengen er omsluttet av ÉN ytre parentes.
      - Bare operatorene 'not', '&', '|'.
      - [ident]-navn: [A-Za-z0-9_]+, ingen whitespace inni '[]'.
      - Parenteser kan nøstes.
      - KRAV: Operatørene 'not', '&', '|' må ha minst ett mellomrom før og etter.
        Eksempler:
          Gyldig:  "( [a] & [b] )", "( not [x] | ( [y] & [z] ) )"
          Ugyldig: "([a]&[b])", "(not [x])", "([a] |[b])"
    """
    s = s.strip()

    # Krav: ytre parentes rundt hele uttrykket
    if not (s.startswith('(') and s.endswith(')')):
        return False
    
    if s=='()' or s=='':
        return True
    
    if '()' not in s:
        print('not empty')
        try:
            tokens = tokenize(s)

            # Ekstra sikkerhet for & og |: sjekk whitespace rundt direkte i tokenlisten
            for idx, tok in enumerate(tokens):
                if tok.kind in ("AND", "OR", "NOT"):
                    # Vi håndhever kravet: minst ett WS-token før og etter
                    # (Selv om parseren også sjekker dette i flyt)
                    require_space_around_operator(tokens, idx)

            parser = Parser(tokens)

            # Parse én ytre '( EXPR )' og sørg for slutt
            if not parser.peek() or parser.peek().kind != 'LPAREN':
                return False
            parser.consume('LPAREN')
            parser.parse_expr()
            parser.optionally_consume_ws()
            if not parser.peek() or parser.peek().kind != 'RPAREN':
                return False
            parser.consume('RPAREN')
            parser.optionally_consume_ws()
            return parser.at_end()

        except ValueError:
            return False
    else: return 
