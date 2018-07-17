#ifndef LM_ENUMERATE_VOCAB_H
#define LM_ENUMERATE_VOCAB_H

#include <string>
#include <vector>

#include "lm/word_index.hh"
#include "util/string_piece.hh"

namespace lm {

/* If you need the actual strings in the vocabulary, inherit from this class
 * and implement Add.  Then put a pointer in Config.enumerate_vocab; it does
 * not take ownership.  Add is called once per vocab word.  index starts at 0
 * and increases by 1 each time.  This is only used by the Model constructor;
 * the pointer is not retained by the class.
 */
class EnumerateVocab {
  public:
    virtual ~EnumerateVocab() {}

    virtual void Add(WordIndex index, const StringPiece &str) = 0;

  protected:
    EnumerateVocab() {}
};

class RetriveStrEnumerateVocab : public EnumerateVocab {
public:
  RetriveStrEnumerateVocab() {}

  void Add(WordIndex index, const StringPiece &str) {
    vocabulary.push_back(std::string(str.data(), str.length()));
  }

  std::vector<std::string> vocabulary;
};

} // namespace lm

#endif // LM_ENUMERATE_VOCAB_H

