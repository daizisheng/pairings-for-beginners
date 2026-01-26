#!/usr/bin/env python3
"""
处理HTML文件，标注CET4以外的词汇
"""

import re
from bs4 import BeautifulSoup, NavigableString

# CET4核心词汇表（约4000词的核心部分）
# 这里包含最常用的词汇，专业术语会被标注
CET4_WORDS = {
    # 基础词汇 A-Z（常见词）
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'must', 'can', 'need', 'dare', 'ought', 'used', 'shall',
    'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around',
    'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond',
    'but', 'by', 'down', 'during', 'except', 'for', 'from', 'in', 'inside',
    'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside',
    'over', 'past', 'since', 'through', 'throughout', 'till', 'to', 'toward',
    'towards', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within',
    'without', 'according',

    # 代词
    'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves',
    'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'whose',
    'this', 'that', 'these', 'those', 'who', 'whom', 'whose', 'which', 'what',
    'whoever', 'whatever', 'whichever', 'where', 'when', 'why', 'how',
    'all', 'another', 'any', 'anybody', 'anyone', 'anything', 'both', 'each',
    'either', 'everybody', 'everyone', 'everything', 'few', 'many', 'most',
    'much', 'neither', 'nobody', 'none', 'nothing', 'one', 'other', 'others',
    'several', 'some', 'somebody', 'someone', 'something', 'such',

    # 连词
    'and', 'or', 'nor', 'so', 'yet', 'for', 'because', 'although', 'though',
    'while', 'whereas', 'if', 'unless', 'whether', 'as', 'than', 'that',
    'after', 'before', 'when', 'whenever', 'where', 'wherever', 'since', 'until',
    'once', 'therefore', 'however', 'moreover', 'furthermore', 'nevertheless',
    'otherwise', 'thus', 'hence', 'accordingly', 'consequently', 'meanwhile',

    # 常用动词
    'accept', 'achieve', 'act', 'add', 'admit', 'affect', 'afford', 'agree',
    'aim', 'allow', 'answer', 'appear', 'apply', 'argue', 'arrive', 'ask',
    'assume', 'attack', 'attempt', 'attend', 'avoid', 'base', 'bear', 'beat',
    'become', 'begin', 'believe', 'belong', 'break', 'bring', 'build', 'burn',
    'buy', 'call', 'care', 'carry', 'catch', 'cause', 'change', 'charge',
    'check', 'choose', 'claim', 'clean', 'clear', 'climb', 'close', 'collect',
    'come', 'compare', 'complete', 'concern', 'consider', 'contain', 'continue',
    'control', 'cook', 'copy', 'cost', 'count', 'cover', 'create', 'cross',
    'cut', 'damage', 'dance', 'deal', 'decide', 'deliver', 'demand', 'depend',
    'describe', 'design', 'destroy', 'develop', 'die', 'discover', 'discuss',
    'divide', 'draw', 'dress', 'drink', 'drive', 'drop', 'eat', 'enable',
    'encourage', 'end', 'enjoy', 'enter', 'establish', 'examine', 'exist',
    'expect', 'experience', 'explain', 'express', 'face', 'fail', 'fall',
    'fear', 'feel', 'fight', 'fill', 'find', 'finish', 'fit', 'fly', 'follow',
    'force', 'forget', 'form', 'gain', 'get', 'give', 'go', 'grow', 'hang',
    'happen', 'hate', 'hear', 'help', 'hide', 'hit', 'hold', 'hope', 'hurt',
    'identify', 'imagine', 'improve', 'include', 'increase', 'indicate',
    'influence', 'inform', 'intend', 'introduce', 'invite', 'involve', 'join',
    'jump', 'keep', 'kill', 'know', 'lack', 'last', 'laugh', 'lay', 'lead',
    'learn', 'leave', 'lend', 'let', 'lie', 'lift', 'link', 'listen', 'live',
    'look', 'lose', 'love', 'make', 'manage', 'mark', 'matter', 'mean', 'measure',
    'meet', 'mention', 'mind', 'miss', 'move', 'notice', 'obtain', 'occur',
    'offer', 'open', 'operate', 'order', 'own', 'pass', 'pay', 'perform',
    'permit', 'pick', 'place', 'plan', 'play', 'point', 'prefer', 'prepare',
    'present', 'press', 'prevent', 'produce', 'promise', 'protect', 'prove',
    'provide', 'publish', 'pull', 'push', 'put', 'raise', 'reach', 'read',
    'realize', 'receive', 'recognize', 'record', 'reduce', 'refer', 'reflect',
    'refuse', 'regard', 'relate', 'release', 'remain', 'remember', 'remove',
    'repeat', 'replace', 'reply', 'report', 'represent', 'require', 'rest',
    'result', 'return', 'reveal', 'ring', 'rise', 'risk', 'run', 'save', 'say',
    'see', 'seek', 'seem', 'sell', 'send', 'separate', 'serve', 'set', 'share',
    'shoot', 'show', 'shut', 'sing', 'sit', 'sleep', 'smile', 'solve', 'sound',
    'speak', 'spend', 'spread', 'stand', 'start', 'state', 'stay', 'steal',
    'stick', 'stop', 'store', 'study', 'succeed', 'suffer', 'suggest', 'suit',
    'supply', 'support', 'suppose', 'surprise', 'surround', 'survive', 'take',
    'talk', 'teach', 'tell', 'tend', 'test', 'thank', 'think', 'throw', 'touch',
    'train', 'travel', 'treat', 'try', 'turn', 'understand', 'use', 'visit',
    'wait', 'walk', 'want', 'warn', 'wash', 'watch', 'wear', 'win', 'wish',
    'wonder', 'work', 'worry', 'write',

    # 常用名词
    'ability', 'account', 'action', 'activity', 'address', 'advantage', 'advice',
    'age', 'air', 'amount', 'analysis', 'animal', 'answer', 'application', 'area',
    'argument', 'arm', 'army', 'art', 'article', 'artist', 'attention', 'audience',
    'author', 'baby', 'back', 'background', 'ball', 'bank', 'base', 'basis',
    'bed', 'beginning', 'behavior', 'belief', 'benefit', 'bird', 'blood', 'board',
    'boat', 'body', 'book', 'bottom', 'box', 'boy', 'brain', 'brother', 'building',
    'business', 'car', 'card', 'care', 'career', 'case', 'cat', 'cause', 'cell',
    'center', 'century', 'chair', 'challenge', 'chance', 'change', 'character',
    'child', 'children', 'choice', 'church', 'city', 'class', 'club', 'coach',
    'college', 'color', 'community', 'company', 'computer', 'concern', 'condition',
    'conference', 'Congress', 'connection', 'control', 'cost', 'country', 'couple',
    'course', 'court', 'culture', 'cup', 'customer', 'data', 'daughter', 'day',
    'deal', 'death', 'decision', 'degree', 'design', 'development', 'difference',
    'director', 'discussion', 'disease', 'doctor', 'dog', 'door', 'dream', 'drive',
    'drug', 'earth', 'east', 'economy', 'edge', 'education', 'effect', 'effort',
    'election', 'employee', 'end', 'energy', 'environment', 'equipment', 'evening',
    'event', 'evidence', 'example', 'exchange', 'executive', 'exercise', 'experience',
    'expert', 'eye', 'face', 'fact', 'factor', 'family', 'fan', 'father', 'fear',
    'feature', 'feeling', 'field', 'figure', 'film', 'fire', 'fish', 'floor',
    'focus', 'food', 'foot', 'force', 'form', 'friend', 'front', 'fund', 'future',
    'game', 'garden', 'girl', 'glass', 'goal', 'god', 'gold', 'government', 'ground',
    'group', 'growth', 'gun', 'guy', 'hair', 'half', 'hand', 'head', 'health',
    'heart', 'heat', 'help', 'history', 'home', 'hope', 'horse', 'hospital', 'hotel',
    'hour', 'house', 'husband', 'idea', 'image', 'impact', 'importance', 'income',
    'increase', 'individual', 'industry', 'information', 'inside', 'instance',
    'institution', 'interest', 'international', 'investment', 'island', 'issue',
    'item', 'job', 'king', 'knowledge', 'land', 'language', 'law', 'lawyer', 'leader',
    'learning', 'leg', 'letter', 'level', 'life', 'light', 'line', 'list', 'little',
    'look', 'loss', 'lot', 'love', 'machine', 'magazine', 'man', 'management',
    'manager', 'market', 'marriage', 'material', 'matter', 'meaning', 'measure',
    'media', 'medical', 'meeting', 'member', 'memory', 'message', 'method', 'middle',
    'military', 'million', 'mind', 'minute', 'model', 'moment', 'money', 'month',
    'morning', 'mother', 'mouth', 'movement', 'movie', 'music', 'name', 'nation',
    'nature', 'need', 'network', 'news', 'newspaper', 'night', 'north', 'note',
    'nothing', 'number', 'office', 'officer', 'oil', 'operation', 'opportunity',
    'option', 'order', 'organization', 'outside', 'owner', 'page', 'pain', 'painting',
    'paper', 'parent', 'park', 'part', 'participant', 'party', 'past', 'patient',
    'pattern', 'peace', 'people', 'performance', 'period', 'person', 'phone',
    'photo', 'picture', 'piece', 'place', 'plan', 'plant', 'player', 'point',
    'police', 'policy', 'politics', 'population', 'position', 'power', 'practice',
    'president', 'pressure', 'price', 'problem', 'process', 'product', 'production',
    'professor', 'program', 'project', 'property', 'public', 'purpose', 'quality',
    'question', 'range', 'rate', 'reader', 'reality', 'reason', 'record', 'region',
    'relationship', 'report', 'research', 'resource', 'response', 'responsibility',
    'rest', 'result', 'return', 'right', 'risk', 'road', 'rock', 'role', 'room',
    'rule', 'sale', 'scene', 'school', 'science', 'scientist', 'sea', 'season',
    'seat', 'second', 'section', 'security', 'sense', 'series', 'service', 'set',
    'sex', 'share', 'shot', 'show', 'side', 'sign', 'significant', 'similar',
    'sister', 'site', 'situation', 'size', 'skill', 'skin', 'society', 'soldier',
    'song', 'son', 'sort', 'sound', 'source', 'south', 'space', 'speech', 'speed',
    'sport', 'staff', 'stage', 'star', 'start', 'state', 'statement', 'station',
    'step', 'stock', 'store', 'story', 'strategy', 'street', 'structure', 'student',
    'study', 'stuff', 'style', 'subject', 'success', 'summer', 'sun', 'surface',
    'system', 'table', 'task', 'tax', 'teacher', 'team', 'technology', 'television',
    'term', 'test', 'text', 'theory', 'thing', 'thought', 'thousand', 'time', 'today',
    'top', 'total', 'town', 'trade', 'training', 'tree', 'trial', 'trip', 'trouble',
    'truth', 'turn', 'type', 'unit', 'university', 'value', 'variety', 'version',
    'view', 'village', 'violence', 'voice', 'wall', 'war', 'water', 'way', 'weapon',
    'week', 'weight', 'west', 'wife', 'will', 'wind', 'window', 'winter', 'woman',
    'women', 'word', 'worker', 'world', 'writer', 'writing', 'yard', 'year', 'youth',

    # 常用形容词
    'able', 'afraid', 'alone', 'angry', 'available', 'aware', 'bad', 'basic',
    'beautiful', 'best', 'better', 'big', 'black', 'blue', 'bright', 'broad',
    'brown', 'busy', 'central', 'certain', 'cheap', 'chief', 'civil', 'clean',
    'clear', 'close', 'cold', 'common', 'complete', 'complex', 'concerned',
    'cool', 'correct', 'current', 'dark', 'dead', 'deep', 'democratic', 'different',
    'difficult', 'direct', 'dry', 'due', 'early', 'easy', 'economic', 'effective',
    'empty', 'entire', 'environmental', 'equal', 'essential', 'european', 'even',
    'exact', 'excellent', 'existing', 'expensive', 'fair', 'false', 'familiar',
    'famous', 'far', 'fast', 'fat', 'federal', 'final', 'financial', 'fine',
    'firm', 'first', 'fit', 'flat', 'following', 'foreign', 'formal', 'former',
    'free', 'fresh', 'front', 'full', 'future', 'general', 'global', 'good',
    'great', 'green', 'grey', 'growing', 'happy', 'hard', 'healthy', 'heavy',
    'helpful', 'high', 'historical', 'hot', 'huge', 'human', 'ill', 'immediate',
    'important', 'impossible', 'independent', 'individual', 'industrial', 'initial',
    'inner', 'interested', 'interesting', 'internal', 'international', 'joint',
    'key', 'kind', 'known', 'large', 'last', 'late', 'later', 'latest', 'leading',
    'least', 'left', 'legal', 'less', 'level', 'likely', 'little', 'living',
    'local', 'long', 'lost', 'low', 'main', 'major', 'male', 'married', 'medical',
    'middle', 'military', 'modern', 'moral', 'narrow', 'national', 'natural',
    'necessary', 'negative', 'new', 'next', 'nice', 'normal', 'northern', 'obvious',
    'official', 'old', 'only', 'open', 'opposite', 'ordinary', 'original', 'other',
    'overall', 'own', 'particular', 'past', 'perfect', 'personal', 'physical',
    'plain', 'planning', 'pleasant', 'political', 'poor', 'popular', 'positive',
    'possible', 'powerful', 'practical', 'present', 'previous', 'primary', 'prime',
    'private', 'professional', 'proper', 'proud', 'public', 'pure', 'quick', 'quiet',
    'rare', 'raw', 'ready', 'real', 'reasonable', 'recent', 'red', 'regional',
    'regular', 'related', 'relative', 'relevant', 'religious', 'remaining',
    'responsible', 'rich', 'right', 'rough', 'round', 'royal', 'sad', 'safe',
    'same', 'scientific', 'secret', 'senior', 'serious', 'severe', 'sexual', 'sharp',
    'short', 'sick', 'significant', 'silent', 'similar', 'simple', 'single', 'slight',
    'slow', 'small', 'smooth', 'social', 'soft', 'solid', 'sorry', 'southern',
    'special', 'specific', 'standard', 'still', 'strange', 'strong', 'successful',
    'sudden', 'sufficient', 'suitable', 'super', 'sure', 'sweet', 'tall', 'technical',
    'terrible', 'thick', 'thin', 'tight', 'tiny', 'top', 'total', 'tough', 'traditional',
    'true', 'typical', 'unable', 'unique', 'united', 'unlikely', 'unusual', 'upper',
    'useful', 'usual', 'valuable', 'various', 'vast', 'warm', 'weak', 'wealthy',
    'western', 'white', 'whole', 'wide', 'wild', 'willing', 'wonderful', 'wooden',
    'working', 'worried', 'worse', 'worst', 'worth', 'wrong', 'yellow', 'young',

    # 常用副词
    'about', 'above', 'absolutely', 'actually', 'again', 'ahead', 'almost', 'alone',
    'along', 'already', 'also', 'always', 'anyway', 'anywhere', 'apparently', 'around',
    'away', 'back', 'badly', 'barely', 'basically', 'behind', 'below', 'beside',
    'better', 'beyond', 'both', 'briefly', 'carefully', 'certainly', 'clearly',
    'closely', 'completely', 'constantly', 'currently', 'deeply', 'definitely',
    'directly', 'down', 'easily', 'effectively', 'either', 'else', 'enough',
    'entirely', 'equally', 'especially', 'essentially', 'even', 'eventually', 'ever',
    'everywhere', 'exactly', 'extremely', 'fairly', 'far', 'finally', 'first',
    'forward', 'fully', 'further', 'generally', 'greatly', 'half', 'hardly', 'heavily',
    'here', 'highly', 'home', 'hopefully', 'however', 'immediately', 'indeed',
    'inside', 'instead', 'just', 'largely', 'last', 'late', 'later', 'least', 'less',
    'likely', 'little', 'long', 'mainly', 'maybe', 'merely', 'more', 'moreover',
    'most', 'mostly', 'much', 'naturally', 'nearly', 'necessarily', 'never',
    'nevertheless', 'next', 'no', 'normally', 'not', 'nothing', 'now', 'obviously',
    'often', 'ok', 'once', 'only', 'originally', 'otherwise', 'out', 'outside',
    'over', 'overall', 'particularly', 'partly', 'perhaps', 'personally', 'please',
    'possibly', 'previously', 'primarily', 'probably', 'properly', 'quickly', 'quite',
    'rarely', 'rather', 'readily', 'really', 'recently', 'relatively', 'seriously',
    'short', 'significantly', 'simply', 'since', 'slightly', 'slowly', 'so',
    'somehow', 'sometimes', 'somewhat', 'somewhere', 'soon', 'specially', 'still',
    'straight', 'strongly', 'subsequently', 'successfully', 'suddenly', 'therefore',
    'thus', 'today', 'together', 'tomorrow', 'tonight', 'too', 'truly', 'typically',
    'ultimately', 'under', 'unfortunately', 'up', 'upon', 'usually', 'very', 'well',
    'whatever', 'whenever', 'widely', 'within', 'without', 'wrong', 'yesterday', 'yet',

    # 数词
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty',
    'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion',
    'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth',
    'ninth', 'tenth', 'once', 'twice', 'double', 'triple', 'half', 'quarter',

    # 学术常用词（CET4范围内）
    'abstract', 'academic', 'access', 'achieve', 'active', 'actual', 'additional',
    'advanced', 'alternative', 'analysis', 'annual', 'appropriate', 'approach',
    'approximately', 'aspect', 'assessment', 'assume', 'attitude', 'authority',
    'average', 'basic', 'benefit', 'brief', 'capable', 'capacity', 'category',
    'chapter', 'characteristic', 'chemical', 'circumstances', 'classic', 'code',
    'comment', 'commit', 'commitment', 'communicate', 'communication', 'component',
    'comprehensive', 'concentrate', 'concept', 'conclusion', 'conduct', 'confirm',
    'conflict', 'considerable', 'consistent', 'constant', 'constitute', 'construct',
    'consumer', 'contact', 'context', 'contract', 'contrast', 'contribute',
    'contribution', 'controversial', 'convention', 'core', 'corporate', 'corresponding',
    'creative', 'credit', 'critical', 'crucial', 'cultural', 'debate', 'decade',
    'define', 'definition', 'demonstrate', 'deny', 'derive', 'despite', 'detail',
    'determine', 'device', 'distinguish', 'distribute', 'document', 'domestic',
    'dominant', 'draft', 'dramatic', 'dynamic', 'element', 'emerge', 'emphasis',
    'ensure', 'entire', 'environment', 'environmental', 'equivalent', 'error',
    'essential', 'establish', 'estimate', 'ethics', 'ethnic', 'evaluate', 'evidence',
    'evolution', 'evolve', 'exclude', 'exhibit', 'expand', 'expansion', 'explicit',
    'explore', 'export', 'expose', 'external', 'extract', 'facility', 'factor',
    'feature', 'federal', 'file', 'final', 'finally', 'finance', 'financial',
    'flexible', 'focus', 'foundation', 'framework', 'function', 'fundamental',
    'fund', 'furthermore', 'generation', 'global', 'grade', 'grant', 'guarantee',
    'guideline', 'hence', 'highlight', 'hypothesis', 'identical', 'identity',
    'ignore', 'illustrate', 'image', 'immigrant', 'implement', 'implication',
    'imply', 'impose', 'incentive', 'incident', 'indicate', 'individual', 'inevitable',
    'infrastructure', 'initial', 'initiative', 'innovation', 'input', 'insight',
    'instance', 'institute', 'institution', 'instruction', 'instrument', 'integrate',
    'intellectual', 'intelligence', 'intense', 'interaction', 'internal', 'interpret',
    'intervention', 'investigate', 'investigation', 'investment', 'involve', 'isolate',
    'issue', 'item', 'journal', 'justify', 'label', 'labor', 'layer', 'lecture',
    'legal', 'legislation', 'liberal', 'likewise', 'link', 'literature', 'locate',
    'location', 'logic', 'maintain', 'maintenance', 'major', 'manual', 'margin',
    'mechanism', 'mental', 'method', 'military', 'minimum', 'minor', 'mode', 'modify',
    'monitor', 'moreover', 'mutual', 'negative', 'network', 'neutral', 'nevertheless',
    'nonetheless', 'norm', 'normal', 'notion', 'nuclear', 'objective', 'obtain',
    'obvious', 'occupy', 'odd', 'offset', 'ongoing', 'option', 'orient', 'original',
    'outcome', 'output', 'overall', 'overseas', 'panel', 'parallel', 'parameter',
    'partial', 'participate', 'participation', 'partner', 'passive', 'perceive',
    'percent', 'percentage', 'perception', 'period', 'permanent', 'perspective',
    'phase', 'phenomenon', 'philosophy', 'physical', 'plus', 'policy', 'portion',
    'pose', 'positive', 'potential', 'practical', 'practice', 'precise', 'predict',
    'preliminary', 'presume', 'primary', 'principal', 'principle', 'prior', 'priority',
    'proceed', 'process', 'professional', 'profit', 'project', 'promote', 'proportion',
    'prospect', 'protocol', 'prove', 'provision', 'psychology', 'publication',
    'pursue', 'qualitative', 'quote', 'radical', 'random', 'ratio', 'rational',
    'react', 'recover', 'recovery', 'reform', 'regime', 'reinforce', 'reject',
    'relevant', 'reliance', 'rely', 'remove', 'require', 'requirement', 'resolution',
    'resolve', 'respectively', 'respond', 'response', 'restore', 'restrict',
    'restriction', 'retain', 'reveal', 'revenue', 'reverse', 'revolution', 'rigid',
    'role', 'route', 'scenario', 'schedule', 'scheme', 'scope', 'sector', 'secure',
    'seek', 'segment', 'select', 'selection', 'sequence', 'series', 'shift',
    'signal', 'significance', 'significant', 'similarly', 'simulate', 'site',
    'somewhat', 'source', 'specific', 'specify', 'spectrum', 'sphere', 'stable',
    'statistics', 'status', 'stimulate', 'straightforward', 'strategy', 'stress',
    'structure', 'style', 'submit', 'subsequent', 'subsidy', 'substitute', 'sufficient',
    'sum', 'summary', 'supplement', 'survey', 'survive', 'suspend', 'sustain',
    'symbol', 'target', 'technical', 'technique', 'temporary', 'tense', 'terminal',
    'theme', 'theoretical', 'thereby', 'thesis', 'topic', 'trace', 'tradition',
    'traditional', 'transfer', 'transform', 'transition', 'transmit', 'transport',
    'trend', 'trigger', 'ultimate', 'undergo', 'underlying', 'undertake', 'uniform',
    'unique', 'utilize', 'valid', 'validity', 'variable', 'variation', 'vary',
    'vehicle', 'version', 'via', 'virtual', 'visible', 'vision', 'visual', 'vital',
    'volume', 'voluntary', 'welfare', 'whereas', 'whereby', 'widespread',

    # 补充常见词
    'chapter', 'section', 'page', 'reader', 'text', 'reading', 'write', 'written',
    'understand', 'understanding', 'understanding', 'learned', 'learning', 'taught',
    'teach', 'teaching', 'shown', 'showing', 'shows', 'example', 'examples',
    'including', 'includes', 'included', 'following', 'follows', 'followed',
    'regarding', 'concerning', 'related', 'relating', 'refers', 'referring',
    'reference', 'references', 'mentioned', 'discusses', 'discussed', 'discussing',
    'provides', 'provided', 'providing', 'gives', 'given', 'giving',
    'presents', 'presented', 'presenting', 'offers', 'offered', 'offering',
    'describes', 'described', 'describing', 'explains', 'explained', 'explaining',
    'introduces', 'introduced', 'introducing', 'covers', 'covered', 'covering',
    'contains', 'contained', 'containing', 'consists', 'consisted', 'consisting',
    'starts', 'started', 'starting', 'begins', 'began', 'beginning', 'ends',
    'ended', 'ending', 'continues', 'continued', 'continuing', 'remains',
    'remained', 'remaining', 'becomes', 'became', 'becoming', 'appears',
    'appeared', 'appearing', 'seems', 'seemed', 'seeming', 'looks', 'looked',
    'looking', 'feels', 'felt', 'feeling', 'sounds', 'sounded', 'sounding',
    'turns', 'turned', 'turning', 'gets', 'got', 'getting', 'makes', 'made',
    'making', 'takes', 'took', 'taking', 'keeps', 'kept', 'keeping', 'lets',
    'letting', 'helps', 'helped', 'helping', 'allows', 'allowed', 'allowing',
    'enables', 'enabled', 'enabling', 'causes', 'caused', 'causing', 'leads',
    'led', 'leading', 'brings', 'brought', 'bringing', 'puts', 'putting',
    'sets', 'setting', 'adds', 'added', 'adding', 'creates', 'created', 'creating',
    'builds', 'built', 'building', 'develops', 'developed', 'developing',
    'produces', 'produced', 'producing', 'forms', 'formed', 'forming',
    'uses', 'used', 'using', 'applies', 'applied', 'applying', 'works',
    'worked', 'working', 'runs', 'ran', 'running', 'plays', 'played', 'playing',
    'serves', 'served', 'serving', 'acts', 'acted', 'acting', 'performs',
    'performed', 'performing', 'functions', 'functioned', 'functioning',
    'operates', 'operated', 'operating', 'moves', 'moved', 'moving', 'changes',
    'changed', 'changing', 'varies', 'varied', 'varying', 'differs', 'differed',
    'differing', 'depends', 'depended', 'depending', 'requires', 'required',
    'requiring', 'needs', 'needed', 'needing', 'wants', 'wanted', 'wanting',
    'likes', 'liked', 'liking', 'loves', 'loved', 'loving', 'enjoys', 'enjoyed',
    'enjoying', 'prefers', 'preferred', 'preferring', 'chooses', 'chose',
    'choosing', 'decides', 'decided', 'deciding', 'considers', 'considered',
    'considering', 'thinks', 'thought', 'thinking', 'believes', 'believed',
    'believing', 'knows', 'knew', 'knowing', 'sees', 'saw', 'seeing', 'finds',
    'found', 'finding', 'discovers', 'discovered', 'discovering', 'learns',
    'learnt', 'notices', 'noticed', 'noticing', 'recognizes', 'recognized',
    'recognizing', 'realizes', 'realized', 'realizing', 'understands', 'understood',

    # 其他常用词
    'actually', 'already', 'also', 'although', 'always', 'another', 'any', 'anyone',
    'anything', 'anyway', 'anywhere', 'apparently', 'around', 'as', 'at', 'away',
    'back', 'be', 'been', 'before', 'being', 'best', 'better', 'between', 'beyond',
    'both', 'but', 'by', 'can', 'cannot', 'certainly', 'could', 'despite', 'did',
    'do', 'does', 'doing', 'done', 'down', 'during', 'each', 'either', 'else',
    'enough', 'especially', 'even', 'ever', 'every', 'everyone', 'everything',
    'everywhere', 'except', 'few', 'first', 'for', 'from', 'further', 'generally',
    'given', 'going', 'good', 'got', 'had', 'has', 'have', 'having', 'he', 'her',
    'here', 'herself', 'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'in',
    'indeed', 'instead', 'into', 'is', 'it', 'its', 'itself', 'just', 'last',
    'later', 'least', 'less', 'let', 'like', 'likely', 'little', 'made', 'make',
    'making', 'many', 'may', 'maybe', 'me', 'might', 'more', 'moreover', 'most',
    'mostly', 'much', 'must', 'my', 'myself', 'nearly', 'necessary', 'neither',
    'never', 'nevertheless', 'new', 'next', 'no', 'nobody', 'none', 'nor', 'not',
    'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
    'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ourselves', 'out', 'over',
    'own', 'particularly', 'perhaps', 'please', 'possible', 'probably', 'quite',
    'rather', 'really', 'said', 'same', 'say', 'says', 'she', 'should', 'since',
    'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometimes',
    'somewhere', 'soon', 'still', 'such', 'sure', 'take', 'taken', 'than', 'that',
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'therefore',
    'these', 'they', 'thing', 'things', 'think', 'this', 'those', 'though',
    'through', 'throughout', 'thus', 'to', 'today', 'together', 'too', 'toward',
    'towards', 'under', 'unless', 'unlike', 'until', 'up', 'upon', 'us', 'used',
    'using', 'usually', 'very', 'want', 'wanted', 'was', 'way', 'ways', 'we',
    'well', 'went', 'were', 'what', 'whatever', 'when', 'whenever', 'where',
    'whereas', 'wherever', 'whether', 'which', 'while', 'who', 'whoever', 'whole',
    'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yes',
    'yet', 'you', 'your', 'yours', 'yourself', 'yourselves',
}

# 非CET4词汇的翻译和音标字典
VOCAB_DICT = {
    # 密码学/数学专业术语
    'aficionados': {'translation': '爱好者，狂热者', 'phonetic': '/əˌfɪʃəˈnɑːdəʊz/'},
    'cryptographic': {'translation': '密码学的', 'phonetic': '/ˌkrɪptəˈɡræfɪk/'},
    'pairing': {'translation': '配对', 'phonetic': '/ˈpeərɪŋ/'},
    'pairings': {'translation': '配对（复数）', 'phonetic': '/ˈpeərɪŋz/'},
    'computation': {'translation': '计算', 'phonetic': '/ˌkɒmpjuˈteɪʃn/'},
    'newcomers': {'translation': '新来者，新手', 'phonetic': '/ˈnjuːˌkʌməz/'},
    'volunteered': {'translation': '自愿提供的', 'phonetic': '/ˌvɒlənˈtɪəd/'},
    'beginner': {'translation': '初学者', 'phonetic': '/bɪˈɡɪnə/'},
    'subset': {'translation': '子集', 'phonetic': '/ˈsʌbset/'},
    'theorems': {'translation': '定理（复数）', 'phonetic': '/ˈθɪərəmz/'},
    'proofs': {'translation': '证明（复数）', 'phonetic': '/pruːfs/'},
    'cryptography': {'translation': '密码学', 'phonetic': '/krɪpˈtɒɡrəfi/'},
    'illustrate': {'translation': '阐明，说明', 'phonetic': '/ˈɪləstreɪt/'},
    'arena': {'translation': '领域，舞台', 'phonetic': '/əˈriːnə/'},
    'pioneering': {'translation': '开创性的', 'phonetic': '/ˌpaɪəˈnɪərɪŋ/'},
    'co-authored': {'translation': '合著的', 'phonetic': '/kəʊˈɔːθəd/'},
    'conveniently': {'translation': '方便地', 'phonetic': '/kənˈviːniəntli/'},
    'algebro-geometric': {'translation': '代数几何的', 'phonetic': '/ˌældʒɪbrəʊ dʒɪəˈmetrɪk/'},
    'webpage': {'translation': '网页', 'phonetic': '/ˈwebpeɪdʒ/'},
    'illustrative': {'translation': '说明性的', 'phonetic': '/ɪˈlʌstrətɪv/'},
    'computations': {'translation': '计算（复数）', 'phonetic': '/ˌkɒmpjuˈteɪʃnz/'},
    'algorithmic': {'translation': '算法的', 'phonetic': '/ˌælɡəˈrɪðmɪk/'},
    'elliptic': {'translation': '椭圆的', 'phonetic': '/ɪˈlɪptɪk/'},
    'concise': {'translation': '简明的', 'phonetic': '/kənˈsaɪs/'},
    'foundational': {'translation': '基础的', 'phonetic': '/faʊnˈdeɪʃənl/'},
    'digging': {'translation': '挖掘，搜寻', 'phonetic': '/ˈdɪɡɪŋ/'},
    'bogged': {'translation': '陷入困境', 'phonetic': '/bɒɡd/'},
    'grasping': {'translation': '理解，掌握', 'phonetic': '/ˈɡrɑːspɪŋ/'},
    'prescribing': {'translation': '规定，开处方', 'phonetic': '/prɪˈskraɪbɪŋ/'},
    'diagnosis': {'translation': '诊断', 'phonetic': '/ˌdaɪəɡˈnəʊsɪs/'},
    'overwhelmed': {'translation': '不知所措的', 'phonetic': '/ˌəʊvəˈwelmd/'},
    'clarity': {'translation': '清晰度', 'phonetic': '/ˈklærəti/'},
    'illuminating': {'translation': '启发性的', 'phonetic': '/ɪˈluːmɪneɪtɪŋ/'},
    'ample': {'translation': '充足的', 'phonetic': '/ˈæmpl/'},
    'jargon': {'translation': '行话，术语', 'phonetic': '/ˈdʒɑːɡən/'},
    'self-contained': {'translation': '自包含的', 'phonetic': '/ˌself kənˈteɪnd/'},
    'digestion': {'translation': '消化，理解', 'phonetic': '/daɪˈdʒestʃən/'},
    'novice': {'translation': '新手', 'phonetic': '/ˈnɒvɪs/'},
    'beneficial': {'translation': '有益的', 'phonetic': '/ˌbenɪˈfɪʃl/'},
    'quadratic': {'translation': '二次的', 'phonetic': '/kwɒˈdrætɪk/'},
    'twisting': {'translation': '扭曲', 'phonetic': '/ˈtwɪstɪŋ/'},
    'isomorphism': {'translation': '同构', 'phonetic': '/ˌaɪsəˈmɔːfɪzəm/'},
    'isomorphisms': {'translation': '同构（复数）', 'phonetic': '/ˌaɪsəˈmɔːfɪzəmz/'},
    'formally': {'translation': '正式地', 'phonetic': '/ˈfɔːməli/'},
    'generality': {'translation': '一般性', 'phonetic': '/ˌdʒenəˈræləti/'},
    'curves': {'translation': '曲线（复数）', 'phonetic': '/kɜːvz/'},
    'curve': {'translation': '曲线', 'phonetic': '/kɜːv/'},
    'machinery': {'translation': '机制，工具', 'phonetic': '/məˈʃiːnəri/'},
    'prelude': {'translation': '前奏，序幕', 'phonetic': '/ˈpreljuːd/'},
    'expositions': {'translation': '论述，阐述', 'phonetic': '/ˌekspəˈzɪʃnz/'},
    'beginner-friendly': {'translation': '对初学者友好的', 'phonetic': '/bɪˈɡɪnə ˈfrendli/'},
    'dissatisfied': {'translation': '不满意的', 'phonetic': '/dɪsˈsætɪsfaɪd/'},
    'formality': {'translation': '形式化', 'phonetic': '/fɔːˈmæləti/'},
    'sacrifice': {'translation': '牺牲', 'phonetic': '/ˈsækrɪfaɪs/'},
    'completeness': {'translation': '完整性', 'phonetic': '/kəmˈpliːtnəs/'},
    'endeavour': {'translation': '努力', 'phonetic': '/ɪnˈdevə/'},
    'thorough': {'translation': '全面的，彻底的', 'phonetic': '/ˈθʌrə/'},
    'exposition': {'translation': '论述，阐述', 'phonetic': '/ˌekspəˈzɪʃn/'},
    'survey': {'translation': '综述，调查', 'phonetic': '/ˈsɜːveɪ/'},
    'decade': {'translation': '十年', 'phonetic': '/ˈdekeɪd/'},
    'fast-paced': {'translation': '快节奏的', 'phonetic': '/fɑːst peɪst/'},
    'mathematicians': {'translation': '数学家（复数）', 'phonetic': '/ˌmæθəməˈtɪʃnz/'},
    'cryptographers': {'translation': '密码学家（复数）', 'phonetic': '/krɪpˈtɒɡrəfəz/'},
    'globe': {'translation': '全球', 'phonetic': '/ɡləʊb/'},
    'maturity': {'translation': '成熟', 'phonetic': '/məˈtʃʊərəti/'},
    'equip': {'translation': '装备，使具备', 'phonetic': '/ɪˈkwɪp/'},
    'tackle': {'translation': '处理，应对', 'phonetic': '/ˈtækl/'},
    'remarkable': {'translation': '卓越的，显著的', 'phonetic': '/rɪˈmɑːkəbl/'},
    'comfortably': {'translation': '舒适地，轻松地', 'phonetic': '/ˈkʌmftəbli/'},
    'absorb': {'translation': '吸收', 'phonetic': '/əbˈzɔːb/'},
    'algebraic': {'translation': '代数的', 'phonetic': '/ˌældʒɪˈbreɪɪk/'},
    'geometry': {'translation': '几何', 'phonetic': '/dʒiˈɒmətri/'},
    'curve-based': {'translation': '基于曲线的', 'phonetic': '/kɜːv beɪst/'},
    'snippet': {'translation': '片段', 'phonetic': '/ˈsnɪpɪt/'},
    'hyperlinked': {'translation': '带超链接的', 'phonetic': '/ˈhaɪpəlɪŋkt/'},
    'tutorial': {'translation': '教程', 'phonetic': '/tjuːˈtɔːriəl/'},
    'encompasses': {'translation': '包含，涵盖', 'phonetic': '/ɪnˈkʌmpəsɪz/'},
    'high-level': {'translation': '高级的', 'phonetic': '/haɪ ˈlevl/'},
    'optimisations': {'translation': '优化（复数）', 'phonetic': '/ˌɒptɪmaɪˈzeɪʃnz/'},
    'culminates': {'translation': '达到高潮', 'phonetic': '/ˈkʌlmɪneɪts/'},
    'organised': {'translation': '组织的', 'phonetic': '/ˈɔːɡənaɪzd/'},
    'overview': {'translation': '概述', 'phonetic': '/ˈəʊvəvjuː/'},
    'divisors': {'translation': '除子（复数）', 'phonetic': '/dɪˈvaɪzəz/'},
    'divisor': {'translation': '除子', 'phonetic': '/dɪˈvaɪzə/'},
    'pairing-friendly': {'translation': '配对友好的', 'phonetic': '/ˈpeərɪŋ ˈfrendli/'},
    'constructing': {'translation': '构造', 'phonetic': '/kənˈstrʌktɪŋ/'},
    'landmark': {'translation': '里程碑式的', 'phonetic': '/ˈlændmɑːk/'},
    'boosted': {'translation': '推动，提升', 'phonetic': '/ˈbuːstɪd/'},
    'calculator': {'translation': '计算器', 'phonetic': '/ˈkælkjuleɪtə/'},
    'scripts': {'translation': '脚本（复数）', 'phonetic': '/skrɪpts/'},
    'online': {'translation': '在线的', 'phonetic': '/ˈɒnlaɪn/'},

    # 人名保持不翻译但提供说明
    'galbraith': {'translation': '（人名）加尔布雷斯', 'phonetic': '/ˈɡælbreɪθ/'},
    'lynn': {'translation': '（人名）林恩', 'phonetic': '/lɪn/'},
    'naehrig': {'translation': '（人名）内里格', 'phonetic': '/ˈneɪrɪɡ/'},
    'scott': {'translation': '（人名）斯科特', 'phonetic': '/skɒt/'},
    'silverman': {'translation': '（人名）西尔弗曼', 'phonetic': '/ˈsɪlvəmən/'},
    'vercauteren': {'translation': '（人名）维尔考特伦', 'phonetic': '/vərˈkaʊtərən/'},
    'dominguez': {'translation': '（人名）多明格斯', 'phonetic': '/dəˈmɪŋɡez/'},
    'perez': {'translation': '（人名）佩雷斯', 'phonetic': '/ˈpereθ/'},
    'magma': {'translation': 'Magma（数学软件）', 'phonetic': '/ˈmæɡmə/'},
    'miller': {'translation': '（人名）米勒', 'phonetic': '/ˈmɪlə/'},
    'weil': {'translation': '（人名）韦伊', 'phonetic': '/veɪl/'},
    'tate': {'translation': '（人名）泰特', 'phonetic': '/teɪt/'},

    # 其他非CET4词汇
    'entitled': {'translation': '题为', 'phonetic': '/ɪnˈtaɪtld/'},
    'aspects': {'translation': '方面（复数）', 'phonetic': '/ˈæspekts/'},
    'sophisticated': {'translation': '复杂的，精密的', 'phonetic': '/səˈfɪstɪkeɪtɪd/'},
    'accordingly': {'translation': '相应地', 'phonetic': '/əˈkɔːdɪŋli/'},
    'picking': {'translation': '挑选', 'phonetic': '/ˈpɪkɪŋ/'},
    'stands': {'translation': '站立，代表', 'phonetic': '/stændz/'},
    'stand-out': {'translation': '杰出的', 'phonetic': '/stænd aʊt/'},
    'toy': {'translation': '简单的，玩具般的', 'phonetic': '/tɔɪ/'},
    'ecc': {'translation': '椭圆曲线密码学', 'phonetic': '/iː siː siː/'},
    'employing': {'translation': '使用，采用', 'phonetic': '/ɪmˈplɔɪɪŋ/'},
    'employed': {'translation': '使用的，采用的', 'phonetic': '/ɪmˈplɔɪd/'},
    'algorithm': {'translation': '算法', 'phonetic': '/ˈælɡərɪðəm/'},
    'notion': {'translation': '概念', 'phonetic': '/ˈnəʊʃn/'},
    'achievements': {'translation': '成就（复数）', 'phonetic': '/əˈtʃiːvmənts/'},
    'improvements': {'translation': '改进（复数）', 'phonetic': '/ɪmˈpruːvmənts/'},
    'aiming': {'translation': '瞄准，针对', 'phonetic': '/ˈeɪmɪŋ/'},
    'matched': {'translation': '匹配的', 'phonetic': '/mætʃt/'},
    'inspiration': {'translation': '灵感', 'phonetic': '/ˌɪnspəˈreɪʃn/'},
    'chapters': {'translation': '章节（复数）', 'phonetic': '/ˈtʃæptəz/'},
    'helpful': {'translation': '有帮助的', 'phonetic': '/ˈhelpfl/'},
    'wherein': {'translation': '在其中', 'phonetic': '/weərˈɪn/'},
    'thesis': {'translation': '论文', 'phonetic': '/ˈθiːsɪs/'},
    'accessing': {'translation': '访问', 'phonetic': '/ˈæksesɪŋ/'},
    'access': {'translation': '访问权限', 'phonetic': '/ˈækses/'},
    'intense': {'translation': '密集的，强烈的', 'phonetic': '/ɪnˈtens/'},
    'racing': {'translation': '快速前进', 'phonetic': '/ˈreɪsɪŋ/'},
    'mapped': {'translation': '映射的', 'phonetic': '/mæpt/'},
    'maps': {'translation': '映射（复数）', 'phonetic': '/mæps/'},
    'straightforward': {'translation': '简单直接的', 'phonetic': '/ˌstreɪtˈfɔːwəd/'},
}

def get_word_info(word):
    """获取单词的翻译和音标"""
    word_lower = word.lower()
    if word_lower in VOCAB_DICT:
        info = VOCAB_DICT[word_lower]
        return info['translation'], info['phonetic']
    # 如果没有找到，返回提示
    return '（专业术语）', ''

def is_cet4_word(word):
    """检查是否是CET4词汇"""
    word_lower = word.lower()
    # 去除常见的词形变化后缀检查
    if word_lower in CET4_WORDS:
        return True
    # 检查一些常见变形
    if word_lower.endswith('s') and word_lower[:-1] in CET4_WORDS:
        return True
    if word_lower.endswith('ed') and word_lower[:-2] in CET4_WORDS:
        return True
    if word_lower.endswith('ed') and word_lower[:-1] in CET4_WORDS:
        return True
    if word_lower.endswith('ing') and word_lower[:-3] in CET4_WORDS:
        return True
    if word_lower.endswith('ing') and word_lower[:-3] + 'e' in CET4_WORDS:
        return True
    if word_lower.endswith('ly') and word_lower[:-2] in CET4_WORDS:
        return True
    if word_lower.endswith('er') and word_lower[:-2] in CET4_WORDS:
        return True
    if word_lower.endswith('est') and word_lower[:-3] in CET4_WORDS:
        return True
    if word_lower.endswith('tion') and word_lower[:-4] + 'te' in CET4_WORDS:
        return True
    if word_lower.endswith('ment') and word_lower[:-4] in CET4_WORDS:
        return True
    if word_lower.endswith('ness') and word_lower[:-4] in CET4_WORDS:
        return True
    if word_lower.endswith('ful') and word_lower[:-3] in CET4_WORDS:
        return True
    if word_lower.endswith('less') and word_lower[:-4] in CET4_WORDS:
        return True
    if word_lower.endswith('able') and word_lower[:-4] in CET4_WORDS:
        return True
    if word_lower.endswith('ible') and word_lower[:-4] in CET4_WORDS:
        return True
    if word_lower.endswith('ive') and word_lower[:-3] + 'e' in CET4_WORDS:
        return True
    if word_lower.endswith('ity') and word_lower[:-3] in CET4_WORDS:
        return True
    if word_lower.endswith("'s") and word_lower[:-2] in CET4_WORDS:
        return True
    return False

def process_text(text, marked_words):
    """处理文本，标注非CET4词汇"""
    # 匹配英文单词（包括连字符词）
    word_pattern = re.compile(r'\b([A-Za-z]+(?:-[A-Za-z]+)*)\b')

    result = []
    last_end = 0

    for match in word_pattern.finditer(text):
        word = match.group(1)
        start, end = match.span()

        # 添加单词前的文本
        result.append(text[last_end:start])

        word_lower = word.lower()

        # 跳过引用标记如 [Gal05]
        if len(word) <= 2 or word.isdigit():
            result.append(word)
        # 检查是否已标注过或是CET4词汇
        elif word_lower in marked_words or is_cet4_word(word):
            result.append(word)
        else:
            # 标注非CET4词汇
            translation, phonetic = get_word_info(word)
            tooltip = f"{phonetic} {translation}" if phonetic else translation
            marked_word = f'<span class="vocab" title="{tooltip}">{word}</span>'
            result.append(marked_word)
            marked_words.add(word_lower)

        last_end = end

    result.append(text[last_end:])
    return ''.join(result)

def process_html(html_content):
    """处理HTML内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    marked_words = set()

    # 添加CSS样式
    style_tag = soup.find('style')
    if style_tag:
        new_css = '''
        .vocab {
            border-bottom: 2px dashed #e74c3c;
            cursor: help;
            position: relative;
        }
        .vocab:hover {
            background-color: #fff3cd;
        }
        '''
        style_tag.string = style_tag.string + new_css

    # 只处理英文段落（不处理blockquote中的中文翻译）
    for p in soup.find_all(['p', 'li']):
        # 跳过blockquote内的内容
        if p.find_parent('blockquote'):
            continue

        # 处理文本节点
        for content in p.contents:
            if isinstance(content, NavigableString):
                parent = content.parent
                if parent.name not in ['span', 'code', 'em']:
                    new_text = process_text(str(content), marked_words)
                    if new_text != str(content):
                        new_soup = BeautifulSoup(new_text, 'html.parser')
                        content.replace_with(new_soup)

    return str(soup)

def main():
    # 读取HTML文件
    with open('/Users/shishengli/pairings-for-beginners/ch1/ch1.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 处理HTML
    processed_html = process_html(html_content)

    # 写入文件
    with open('/Users/shishengli/pairings-for-beginners/ch1/ch1.html', 'w', encoding='utf-8') as f:
        f.write(processed_html)

    print("处理完成！")

if __name__ == '__main__':
    main()
