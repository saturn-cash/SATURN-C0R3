# Libraries

| Name                     | Description |
|--------------------------|-------------|
| *libsaturn_cli*         | RPC client functionality used by *saturn-cli* executable |
| *libsaturn_common*      | Home for common functionality shared by different executables and libraries. Similar to *libsaturn_util*, but higher-level (see [Dependencies](#dependencies)). |
| *libsaturn_consensus*   | Consensus functionality used by *libsaturn_node* and *libsaturn_wallet*. |
| *libsaturn_crypto*      | Hardware-optimized functions for data encryption, hashing, message authentication, and key derivation. |
| *libsaturn_kernel*      | Consensus engine and support library used for validation by *libsaturn_node*. |
| *libsaturnqt*           | GUI functionality used by *saturn-qt* and *saturn-gui* executables. |
| *libsaturn_ipc*         | IPC functionality used by *saturn-node* and *saturn-gui* executables to communicate when [`-DENABLE_IPC=ON`](multiprocess.md) is used. |
| *libsaturn_node*        | P2P and RPC server functionality used by *saturnd* and *saturn-qt* executables. |
| *libsaturn_util*        | Home for common functionality shared by different executables and libraries. Similar to *libsaturn_common*, but lower-level (see [Dependencies](#dependencies)). |
| *libsaturn_wallet*      | Wallet functionality used by *saturnd* and *saturn-wallet* executables. |
| *libsaturn_wallet_tool* | Lower-level wallet functionality used by *saturn-wallet* executable. |
| *libsaturn_zmq*         | [ZeroMQ](../zmq.md) functionality used by *saturnd* and *saturn-qt* executables. |

## Conventions

- Most libraries are internal libraries and have APIs which are completely unstable! There are few or no restrictions on backwards compatibility or rules about external dependencies. An exception is *libsaturn_kernel*, which, at some future point, will have a documented external interface.

- Generally each library should have a corresponding source directory and namespace. Source code organization is a work in progress, so it is true that some namespaces are applied inconsistently, and if you look at [`add_library(saturn_* ...)`](../../src/CMakeLists.txt) lists you can see that many libraries pull in files from outside their source directory. But when working with libraries, it is good to follow a consistent pattern like:

  - *libsaturn_node* code lives in `src/node/` in the `node::` namespace
  - *libsaturn_wallet* code lives in `src/wallet/` in the `wallet::` namespace
  - *libsaturn_ipc* code lives in `src/ipc/` in the `ipc::` namespace
  - *libsaturn_util* code lives in `src/util/` in the `util::` namespace
  - *libsaturn_consensus* code lives in `src/consensus/` in the `Consensus::` namespace

## Dependencies

- Libraries should minimize what other libraries they depend on, and only reference symbols following the arrows shown in the dependency graph below:

<table><tr><td>

```mermaid

%%{ init : { "flowchart" : { "curve" : "basis" }}}%%

graph TD;

saturn-cli[saturn-cli]-->libsaturn_cli;

saturnd[saturnd]-->libsaturn_node;
saturnd[saturnd]-->libsaturn_wallet;

saturn-qt[saturn-qt]-->libsaturn_node;
saturn-qt[saturn-qt]-->libsaturnqt;
saturn-qt[saturn-qt]-->libsaturn_wallet;

saturn-wallet[saturn-wallet]-->libsaturn_wallet;
saturn-wallet[saturn-wallet]-->libsaturn_wallet_tool;

libsaturn_cli-->libsaturn_util;
libsaturn_cli-->libsaturn_common;

libsaturn_consensus-->libsaturn_crypto;

libsaturn_common-->libsaturn_consensus;
libsaturn_common-->libsaturn_crypto;
libsaturn_common-->libsaturn_util;

libsaturn_kernel-->libsaturn_consensus;
libsaturn_kernel-->libsaturn_crypto;
libsaturn_kernel-->libsaturn_util;

libsaturn_node-->libsaturn_consensus;
libsaturn_node-->libsaturn_crypto;
libsaturn_node-->libsaturn_kernel;
libsaturn_node-->libsaturn_common;
libsaturn_node-->libsaturn_util;

libsaturnqt-->libsaturn_common;
libsaturnqt-->libsaturn_util;

libsaturn_util-->libsaturn_crypto;

libsaturn_wallet-->libsaturn_common;
libsaturn_wallet-->libsaturn_crypto;
libsaturn_wallet-->libsaturn_util;

libsaturn_wallet_tool-->libsaturn_wallet;
libsaturn_wallet_tool-->libsaturn_util;

classDef bold stroke-width:2px, font-weight:bold, font-size: smaller;
class saturn-qt,saturnd,saturn-cli,saturn-wallet bold
```
</td></tr><tr><td>

**Dependency graph**. Arrows show linker symbol dependencies. *Crypto* lib depends on nothing. *Util* lib is depended on by everything. *Kernel* lib depends only on consensus, crypto, and util.

</td></tr></table>

- The graph shows what _linker symbols_ (functions and variables) from each library other libraries can call and reference directly, but it is not a call graph. For example, there is no arrow connecting *libsaturn_wallet* and *libsaturn_node* libraries, because these libraries are intended to be modular and not depend on each other's internal implementation details. But wallet code is still able to call node code indirectly through the `interfaces::Chain` abstract class in [`interfaces/chain.h`](../../src/interfaces/chain.h) and node code calls wallet code through the `interfaces::ChainClient` and `interfaces::Chain::Notifications` abstract classes in the same file. In general, defining abstract classes in [`src/interfaces/`](../../src/interfaces/) can be a convenient way of avoiding unwanted direct dependencies or circular dependencies between libraries.

- *libsaturn_crypto* should be a standalone dependency that any library can depend on, and it should not depend on any other libraries itself.

- *libsaturn_consensus* should only depend on *libsaturn_crypto*, and all other libraries besides *libsaturn_crypto* should be allowed to depend on it.

- *libsaturn_util* should be a standalone dependency that any library can depend on, and it should not depend on other libraries except *libsaturn_crypto*. It provides basic utilities that fill in gaps in the C++ standard library and provide lightweight abstractions over platform-specific features. Since the util library is distributed with the kernel and is usable by kernel applications, it shouldn't contain functions that external code shouldn't call, like higher level code targeted at the node or wallet. (*libsaturn_common* is a better place for higher level code, or code that is meant to be used by internal applications only.)

- *libsaturn_common* is a home for miscellaneous shared code used by different Saturn Core applications. It should not depend on anything other than *libsaturn_util*, *libsaturn_consensus*, and *libsaturn_crypto*.

- *libsaturn_kernel* should only depend on *libsaturn_util*, *libsaturn_consensus*, and *libsaturn_crypto*.

- The only thing that should depend on *libsaturn_kernel* internally should be *libsaturn_node*. GUI and wallet libraries *libsaturnqt* and *libsaturn_wallet* in particular should not depend on *libsaturn_kernel* and the unneeded functionality it would pull in, like block validation. To the extent that GUI and wallet code need scripting and signing functionality, they should be able to get it from *libsaturn_consensus*, *libsaturn_common*, *libsaturn_crypto*, and *libsaturn_util*, instead of *libsaturn_kernel*.

- GUI, node, and wallet code internal implementations should all be independent of each other, and the *libsaturnqt*, *libsaturn_node*, *libsaturn_wallet* libraries should never reference each other's symbols. They should only call each other through [`src/interfaces/`](../../src/interfaces/) abstract interfaces.

## Work in progress

- Validation code is moving from *libsaturn_node* to *libsaturn_kernel* as part of [The libsaturnkernel Project #27587](https://github.com/saturn/saturn/issues/27587)
