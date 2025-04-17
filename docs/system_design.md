# docs/system_design.md
## Multichain Order Book Architecture

### Components:
1. **Order Manager**: Handles order routing and validation
2. **Chain Adapters**: Blockchain-specific communication
3. **Settlement Engine**: Atomic cross-chain transactions
4. **Risk Engine**: Monitors liquidity and gas costs

### Workflow:
1. User submits order with gas budget
2. System validates asset-chain pairs
3. Order book matches with best available price
4. Cross-chain settlement executed
5. Transaction status monitored